from fasthtml.common import *


_HEAD = (
    Link(rel="preconnect", href="https://fonts.googleapis.com"),
    Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
    Link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@0;1&display=swap"),
    Style("""
        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            background: #f5f0e8;
            color: #2c2016;
            font-family: 'IM Fell English', serif;
            font-size: 1.15rem;
            line-height: 1.8;
        }

        .reader {
            max-width: 680px;
            margin: 2rem auto;
            padding: 0 1.5rem;
        }

        .nav {
            display: flex;
            justify-content: space-between;
            margin-bottom: 2rem;
            border-bottom: 1px solid #8b7355;
            padding-bottom: 1rem;
        }

        .nav button {
            background: none;
            border: 1px solid #8b7355;
            color: #2c2016;
            font-family: 'IM Fell English', serif;
            font-size: 0.95rem;
            padding: 0.3rem 1rem;
            cursor: pointer;
            letter-spacing: 0.05em;
        }

        .nav button:hover { background: #e8dfc8; }

        .nav .page-info {
            font-size: 0.9rem;
            color: #6b5a3e;
            align-self: center;
            font-style: italic;
        }

        pre.content {
            font-family: 'IM Fell English', serif;
            font-size: 1.15rem;
            line-height: 1.8;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
    """),
)

_BRIDGE_JS = """
import { App } from "https://cdn.jsdelivr.net/npm/@modelcontextprotocol/ext-apps@latest/+esm";

const app = new App({ name: "reader", version: "1.0.0" });
app.connect();

function updateNav(page_number, total_pages) {
    document.getElementById("prev-page").value = Math.max(1, page_number - 1);
    document.getElementById("next-page").value = Math.min(total_pages, page_number + 1);
    document.getElementById("page-info").textContent = `Page ${page_number} of ${total_pages}`;
}

function syncModelContext(page_number, total_pages) {
    app.updateModelContext({ structuredContent: { page_number, total_pages } });
}

// LLM-initiated tool call result pushed by host
app.ontoolresult = (result) => {
    const meta = result._meta ?? {};
    document.getElementById("content").innerHTML = meta.html ?? "";
    if (meta.page_number) {
        updateNav(meta.page_number, meta.total_pages);
        syncModelContext(meta.page_number, meta.total_pages);
    }
};

// User-initiated via Fixi button click
document.addEventListener("fx:config", (evt) => {
    const action = evt.detail.cfg.action;
    if (!action?.startsWith("tool:")) return;
    const toolName = action.slice(5);
    const form = evt.target.closest("form");
    const raw = Object.fromEntries(new FormData(form));
    const args = { ...raw, page_number: parseInt(raw.page_number) };

    // Override cfg.fetch — Fixi always calls cfg.fetch(), setting cfg.response here has no effect
    evt.detail.cfg.fetch = () => app.callServerTool({ name: toolName, arguments: args })
        .then(result => {
            const meta = result._meta ?? {};
            if (meta.page_number) {
                updateNav(meta.page_number, meta.total_pages);
                syncModelContext(meta.page_number, meta.total_pages);
            }
            return new Response(meta.html ?? "", {
                headers: { "content-type": "text/html" },
            });
        });
});
"""


def render_shell() -> str:
    """Full HTML app shell — served once as ui://reader resource."""
    page = Html(
        Head(
            Title("The Pavilion on the Links"),
            *_HEAD,
            Script(src="https://cdn.jsdelivr.net/npm/fixi-js@latest/fixi.js"),
            Script(NotStr(_BRIDGE_JS), type="module"),
        ),
        Body(
            Main(
                Div(
                    Form(
                        Input(type="hidden", name="page_number", id="prev-page", value="1"),
                        Button("← Previous", type="submit"),
                        fx_action="tool:reader",
                        fx_target="#content",
                        fx_swap="innerHTML",
                    ),
                    Span("", id="page-info", cls="page-info"),
                    Form(
                        Input(type="hidden", name="page_number", id="next-page", value="2"),
                        Button("Next →", type="submit"),
                        fx_action="tool:reader",
                        fx_target="#content",
                        fx_swap="innerHTML",
                    ),
                    cls="nav",
                ),
                Div(id="content", cls="content"),
                cls="reader",
            )
        ),
    )
    return to_xml(page)
