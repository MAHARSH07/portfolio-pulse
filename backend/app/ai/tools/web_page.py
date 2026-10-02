from langchain_core.tools import tool

from app.web.page_fetcher import WebPageFetcher


@tool
def fetch_web_page_tool(url: str) -> dict:
    """
    Fetch the readable text content of a webpage from a URL.

    Use this after web search when a search result needs deeper
    inspection than the search snippet provides.
    """

    fetcher = WebPageFetcher()
    content = fetcher.fetch(url)

    return {
        "url": url,
        "content": content,
        "character_count": len(content),
    }