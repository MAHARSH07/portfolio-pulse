from langchain_core.tools import tool

from app.web.providers.factory import get_web_search_provider
from app.web.service import WebSearchService


@tool
def search_web_tool(
    query: str,
    topic: str = "general",
    days: int | None = None,
) -> dict:
    """
    Search the live web for current information, news, company information,
    announcements, reports, and other publicly available information.

    Use this tool when the user's question requires information that may
    have changed recently or is not available in the portfolio database.

    Use topic="news" for recent news and news coverage.

    Use days to restrict results to a recent time window when freshness
    matters. For example, days=7 searches for recent information from the
    last 7 days.

    Use topic="general" for general web research.
    """
    provider = get_web_search_provider()
    service = WebSearchService(provider)

    result = service.search(
        query=query,
        topic=topic,
        days=days,
    )

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
