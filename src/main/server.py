from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field
from fastmcp import FastMCP

mcp = FastMCP("mcp-app-dynamic-ui")

LINES_PER_PAGE = 40
_lines = Path("src/data/pavilion.txt").read_text(encoding="utf-8").splitlines()
TOTAL_PAGES = (len(_lines) + LINES_PER_PAGE - 1) // LINES_PER_PAGE


class Page(BaseModel):
    page_number: int
    total_pages: int
    content: str


@mcp.tool
def reader(page_number: Annotated[int, Field(ge=1, description="Page number, starting at 1")]) -> Page:
    """Read 'The Pavilion on the Links' by Robert Louis Stevenson.
    Allows interactive reading of the story page by page."""
    start = (page_number - 1) * LINES_PER_PAGE
    content = "\n".join(_lines[start: start + LINES_PER_PAGE])
    return Page(page_number=page_number, total_pages=TOTAL_PAGES, content=content)


if __name__ == "__main__":
    mcp.run()
