from pydantic import BaseModel
from fastmcp import FastMCP

mcp = FastMCP("mcp-app-dynamic-ui")


class Page(BaseModel):
    page_number: int
    content: str


@mcp.tool
def reader(page_number: int) -> Page:
    """Read 'The Pavilion on the Links' by Robert Louis Stevenson.
    Allows interactive reading of the story page by page."""
    return Page(page_number=page_number, content="")


if __name__ == "__main__":
    mcp.run()
