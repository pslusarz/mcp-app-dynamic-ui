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

Then start the MCP Inspector:

```sh
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
export PATH="/Users/pjs/.local/bin:$PATH"
mcp-inspector uv run src/main/server.py
```

The inspector UI will be available at **http://localhost:6274**.

After changing code, click **Reconnect** in the inspector UI — it spawns a fresh server process each time, so you always get the latest code.

## Known Issues

**Do NOT use `uv run --watch` or `fastmcp run --reload` with the inspector.**
- `uv run --watch` breaks the stdio pipe (`EPIPE`) and triggers an endless reconnect loop
- `fastmcp run --reload` crashes the inspector's Node process entirely with `Error: Not connected` when a reload fires mid-connection

Both approaches kill the inspector. The simple fix: just click Reconnect in the UI after code changes.

## Troubleshooting

- **Port already in use**: run the kill commands above before starting
- **EPIPE / endless reconnect loop**: you used `--watch` — kill everything and restart without it
- **Inspector opens but no tools visible**: check the server started cleanly by running `uv run src/main/server.py` directly first
