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
mcp-inspector uv run fastmcp run src/main/server.py --reload
```

The inspector UI will be available at **http://localhost:6274**.

After saving a file, FastMCP restarts cleanly. Click **Reconnect** in the inspector UI to pick up the changes.

## Known Issues

**Do NOT use `uv run --watch` with the inspector.**
The inspector uses stdio transport — it spawns the server as a subprocess per connection. The `--watch` flag causes uv to restart the server process on file changes, which breaks the stdio pipe (`EPIPE` error). This triggers an endless reconnect loop flooding the logs.

**Why `fastmcp run --reload` works instead:** FastMCP handles the reload internally without killing the outer process, so the stdio pipe stays intact.

## Troubleshooting

- **Port already in use**: run the kill commands above before starting
- **EPIPE / endless reconnect loop**: you used `--watch` — kill everything and restart without it
- **Inspector opens but no tools visible**: check the server started cleanly by running `uv run src/main/server.py` directly first
