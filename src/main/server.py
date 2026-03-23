import logging
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field
from fastmcp import FastMCP
from fastmcp.tools.tool import ToolResult
from mcp.types import TextContent
from templates import render_shell, render_fragment

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[
        logging.FileHandler("logs/server.log"),
        logging.StreamHandler(),
    ],
)

mcp = FastMCP(
    "mcp-app-dynamic-ui",
    version="0.1.0",
    instructions=(
        "This server provides interactive reading of 'The Pavilion on the Links' "
        "by Robert Louis Stevenson. Use the reader tool to fetch pages by number."
    ),
)

LINES_PER_PAGE = 40
_lines = Path("src/data/pavilion.txt").read_text(encoding="utf-8").splitlines()
TOTAL_PAGES = (len(_lines) + LINES_PER_PAGE - 1) // LINES_PER_PAGE


class Page(BaseModel):
    page_number: int
    total_pages: int
    content: str


@mcp.resource("ui://reader", mime_type="text/html;profile=mcp-app")
def reader_ui() -> str:
    return render_shell()


@mcp.tool(meta={"ui": {"resourceUri": "ui://reader"}})
def reader(page_number: Annotated[int, Field(ge=1, description="Page number, starting at 1")]) -> ToolResult:
    """Read 'The Pavilion on the Links' by Robert Louis Stevenson.
    Allows interactive reading of the story page by page."""
    start = (page_number - 1) * LINES_PER_PAGE
    content = "\n".join(_lines[start: start + LINES_PER_PAGE])
    page = Page(page_number=page_number, total_pages=TOTAL_PAGES, content=content)
    return ToolResult(
        content=[TextContent(type="text", text=f"Page {page_number} of {TOTAL_PAGES}")],
        structured_content=page.model_dump(),
        meta={"html": render_fragment(content)},
    )


if __name__ == "__main__":
    mcp.run()
