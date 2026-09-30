from langchain_core.tools import tool

from app.web.providers.tavily import TavilySearchProvider
from app.web.service import WebSearchService


@tool
def search_web_tool(query: str) -> dict:
    """
    Search the live web for current information, news, company information,
    announcements, reports, and other publicly available information.
    Use this tool when the user's question requires information that may
    have changed recently or is not available in the portfolio database.
    """
    provider = TavilySearchProvider()
    service = WebSearchService(provider)

    result = service.search(query)

    return {
        "query": result.query,
        "results": [
            {
                "title": item.title,
                "url": item.url,
                "description": item.description,
                "source": item.source,
                "published_at": (
                    item.published_at.isoformat()
                    if item.published_at
                    else None
                ),
            }
            for item in result.results
        ],
    }