from fastmcp import FastMCP

mcp = FastMCP("mcp-app-dynamic-ui")


@mcp.tool()
def foo() -> str:
    return "bar"


if __name__ == "__main__":
    mcp.run()
