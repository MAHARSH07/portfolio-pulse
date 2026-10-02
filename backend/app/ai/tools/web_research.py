from langchain_core.tools import tool

from app.web.page_fetcher import WebPageFetcher
from app.web.providers.factory import get_web_search_provider
from app.web.ranking import rank_search_results
from app.web.service import WebSearchService


@tool
def research_web_tool(
    query: str,
    topic: str = "general",
    days: int | None = None,
) -> dict:
    """
    Search the live web and inspect the most relevant pages in depth.

    Use this for questions that require recent news, current events,
    company developments, market information, or deeper web research.
    """

    provider = get_web_search_provider()
    search_service = WebSearchService(provider)

    search_result = search_service.search(
        query=query,
        topic=topic,
        days=days,
    )

    ranked_results = rank_search_results(
        results=search_result.results,
        query=query,
        topic=topic,
    )

    page_fetcher = WebPageFetcher()

    research_results = []

    for result in ranked_results:
        try:
            content = page_fetcher.fetch(result.url)

            research_results.append(
                {
                    "title": result.title,
                    "url": result.url,
                    "source": result.source,
                    "description": result.description,
                    "published_at": (
                        result.published_at.isoformat()
                        if result.published_at
                        else None
                    ),
                    "content": content,
                }
            )

        except Exception as exc:
            print(
                f"Failed to fetch {result.url}: {exc}"
            )
            continue

        if len(research_results) >= 2:
            break

    return {
        "query": search_result.query,
        "results": research_results,
    }