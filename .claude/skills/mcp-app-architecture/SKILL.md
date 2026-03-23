---
name: mcp-app-architecture
description: Reference this skill when deep understanding is needed for the data flow between mcp host, the llm, the user's browser, and the mcp server.
---

## Overview

An MCP App is a tool with an associated UI resource. The host (e.g. Claude Desktop) renders the UI in a sandboxed iframe and mediates all communication between the LLM, the user's browser, and the MCP server.

## Data Flow

```
User browser (iframe)
      ↕  postMessage / JSON-RPC
MCP Host (e.g. Claude Desktop)
      ↕  MCP protocol
MCP Server (our FastMCP Python server)
      ↕  internal
LLM
```

### On page load
1. Host calls `tools/list` → receives tool definitions including `_meta.ui.resourceUri`
2. Host fetches `ui://reader` resource from server → gets the HTML shell
3. Host renders the shell in a sandboxed iframe
4. Shell calls `app.connect()` to establish postMessage channel with host

### On tool call (LLM or user-initiated)
1. Host calls `tools/call` on the server with arguments
2. Server returns a `ToolResult` with:
   - `content` — plain text summary (appears in conversation transcript, model sees it)
   - `structured_content` — typed data (appears in transcript, model sees it)
   - `meta` — arbitrary data forwarded to iframe only, **model never sees this**
3. Host pushes result into the iframe via `ui/notifications/tool-result`
4. Shell's `app.ontoolresult` callback fires with the result
5. Shell swaps `result._meta.html` (pre-rendered HTML fragment) into the content div

### On button click (Fixi)
1. User clicks Prev/Next (rendered with `fx-action="tool:reader"`)
2. Fixi intercepts via `fx:config` event listener
3. Bridge code calls `app.callServerTool({ name: "reader", arguments: { page_number: N } })`
4. Same flow as above from step 1

## Key Rules

- **`_meta.ui.resourceUri` is fixed at tool definition time** — the host may preload the resource before the tool runs. It cannot vary per call.
- **The UI shell is static** — it contains layout, JS, and Fixi. It does not render data itself.
- **Data arrives via postMessage** — never via HTTP from inside the iframe.
- **`meta` in tool response is UI-only** — use it for pre-rendered HTML fragments. The LLM never sees it.
- **`structured_content` is for the model** — clean typed data the LLM can reason about.
- **mime_type must be `text/html;profile=mcp-app`** — not plain `text/html`.

## Our Implementation Pattern

```python
# Tool returns structured data for the model + HTML fragment for the UI
@mcp.tool(meta={"ui": {"resourceUri": "ui://reader"}})
def reader(page_number: int) -> ToolResult:
    content = get_page_lines(page_number)
    return ToolResult(
        content=[TextContent(type="text", text=f"Page {page_number}")],
        structured_content=Page(page_number=page_number, ...),
        meta={"html": render_fragment(page_number, total_pages, content)},
    )

# Static shell served once
@mcp.resource("ui://reader", mime_type="text/html;profile=mcp-app")
def reader_ui() -> str:
    return render_shell()  # layout + Fixi + app.connect() JS only
```

```javascript
// Inside the shell
const app = new App({ name: "reader", version: "1.0.0" });
app.connect();

app.ontoolresult = (result) => {
    document.getElementById("content").innerHTML = result._meta.html;
};

// Fixi bridge — routes fx-action="tool:*" through app.callServerTool
document.addEventListener("fx:config", async (evt) => {
    const action = evt.detail.cfg.url;
    if (!action.startsWith("tool:")) return;
    const toolName = action.slice(5);
    const args = Object.fromEntries(new FormData(evt.target.closest("form")));
    evt.detail.cfg.response = app.callServerTool({ name: toolName, arguments: args })
        .then(r => new Response(r._meta?.html ?? "", { headers: { "content-type": "text/html" } }));
});
```

## Template Structure

- `render_shell(total_pages)` → full HTML page with nav, empty content div, Fixi, SDK, bridge JS
- `render_fragment(page_number, total_pages, content)` → just the content area HTML, swapped in per tool call

## References

- MCP Apps spec: https://modelcontextprotocol.io/docs/extensions/apps
- Fixi library: https://github.com/bigskysoftware/fixi
- HTMX essay on MCP Apps: https://htmx.org/essays/mcp-apps-hypermedia/
- ext-apps SDK: https://github.com/modelcontextprotocol/ext-apps
