---
name: local-server-development
description: Instructions for running and developing the MCP server locally, including the inspector.
---

## Running the Server Locally

Before starting, kill any existing inspector or server processes and free the ports:

```sh
lsof -ti:6274 -ti:6277 | xargs kill -9 2>/dev/null
pkill -f "src/main/server.py" 2>/dev/null
sleep 1
```

Then start the MCP Inspector, logging all output to `logs/inspector.log`:

```sh
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
export PATH="/Users/pjs/.local/bin:$PATH"
mcp-inspector uv run src/main/server.py 2>&1 | tee logs/inspector.log
```

The inspector UI will be available at **http://localhost:6274**.

To watch the log in real time in a separate terminal:
```sh
tail -f logs/inspector.log
```

After changing code, click **Reconnect** in the inspector UI — it spawns a fresh server process each time, so you always get the latest code.

## Known Issues

**Do NOT use `uv run --watch` or `fastmcp run --reload` with the inspector.**
- `uv run --watch` breaks the stdio pipe (`EPIPE`) and triggers an endless reconnect loop
- `fastmcp run --reload` crashes the inspector's Node process entirely with `Error: Not connected` when a reload fires mid-connection

Both approaches kill the inspector. The simple fix: just click Reconnect in the UI after code changes.

## Verifying server changes without restarting inspector

The inspector log only captures the Node.js proxy layer — Python server stderr is not visible there. To verify a code change before reconnecting:

```sh
uv run python -c "
import sys, asyncio
sys.path.insert(0, 'src/main')
import server
loop = asyncio.new_event_loop()
print('Tools:', [t.name for t in loop.run_until_complete(server.mcp.list_tools())])
print('Resources:', [r.uri for r in loop.run_until_complete(server.mcp.list_resources())])
"
```

If this fails, fix the error before reconnecting. If it succeeds, reconnect in the inspector UI.

For full server logs (FastMCP startup messages, runtime errors), run the server directly in a separate terminal:
```sh
uv run src/main/server.py
```

## Debugging MCP Inspector UI/Apps errors

First check `logs/inspector.log` — all inspector stdout/stderr goes there. For errors thrown in the browser-side renderer, grep the inspector source:

```sh
grep -r "Unsupported\|Error\|mcp-app" \
  ~/.nvm/versions/node/v24.14.0/lib/node_modules/@modelcontextprotocol/inspector/node_modules/@mcp-ui/client/dist/index.js \
  2>/dev/null | head -20
```

Key file locations inside the inspector install:
- `~/.nvm/versions/node/v24.14.0/lib/node_modules/@modelcontextprotocol/inspector/node_modules/@mcp-ui/client/dist/index.js` — UI resource rendering logic
- `~/.nvm/versions/node/v24.14.0/lib/node_modules/@modelcontextprotocol/inspector/client/dist/assets/index-uKaJPCZp.js` — inspector client bundle

**Known requirement:** UI resources must use `mime_type="text/html;profile=mcp-app"` (not plain `"text/html"`). The inspector checks for the `profile=mcp-app` suffix before rendering.

## Troubleshooting

- **Port already in use**: run the kill commands above before starting
- **EPIPE / endless reconnect loop**: you used `--watch` — kill everything and restart without it
- **Inspector opens but no tools visible**: check the server started cleanly by running `uv run src/main/server.py` directly first
- **"Unsupported UI resource content format"**: check `mime_type` — must be `"text/html;profile=mcp-app"`, not `"text/html"`
