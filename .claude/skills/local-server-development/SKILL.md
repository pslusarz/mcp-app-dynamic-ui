---
name: local-server-development
description: Instructions for running and developing the MCP server locally, including the inspector.
---

## Running the Server Locally

Before starting the server, check if a previous instance is already running and kill it:

```sh
pkill -f "src/main/server.py" 2>/dev/null || true
```

Then start the server with the MCP Inspector and auto-reload on file changes:

```sh
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
export PATH="/Users/pjs/.local/bin:$PATH"
mcp-inspector uv run --watch src/main/server.py
```

The inspector UI will be available at **http://localhost:6274**.
