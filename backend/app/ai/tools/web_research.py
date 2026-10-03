from datetime import datetime, timezone

from langchain_core.tools import tool

from app.web.page_fetcher import WebPageFetcher
from app.web.providers.factory import get_web_search_provider
from app.web.ranking import rank_search_results
from app.web.service import WebSearchService
from app.web.schemas import WebSearchResult


GENERIC_QUERY_TERMS = {
    "latest",
    "recent",
    "today",
    "news",
    "developments",
    "development",
    "earnings",
    "results",
    "partnerships",
    "partnership",
    "updates",
    "update",
    "stock",
    "share",
    "price",
    "market",
}


def _extract_entity_query(query: str) -> str:
    """
    Extract the likely company/entity portion from a search query.

    Example:

        "KPIT Technologies latest news developments earnings"

    becomes:

        "KPIT Technologies"
    """

    words = [
        word.strip()
        for word in query.split()
        if len(word.strip()) > 2
    ]

    entity_words = []

    for word in words:
        if word.lower() in GENERIC_QUERY_TERMS:
            break

        entity_words.append(word)

    return " ".join(entity_words)


def _contains_entity(
    result: WebSearchResult,
    entity_query: str,
) -> bool:
    """
    Check whether a search result actually refers to the
    requested company/entity.
    """

    entity_terms = [
        term.lower()
        for term in entity_query.split()
        if len(term) > 2
    ]

    if not entity_terms:
        return True

    title = result.title.lower()
    description = (result.description or "").lower()

    # Prefer the complete entity phrase.
    entity_phrase = " ".join(entity_terms)

    if entity_phrase in title or entity_phrase in description:
        return True

    # Fall back to the first, usually most distinctive,
    # company/entity term.
    distinctive_term = entity_terms[0]

    return (
        distinctive_term in title
        or distinctive_term in description
    )


def _build_source(
    source_number: int,
    result: WebSearchResult,
    content: str,
) -> dict:
    """
    Convert one successfully fetched webpage into an explicitly
    identified research source.

    The search-result description is intentionally not included.

    Search-result descriptions can contain unrelated snippets such
    as "More News", recommendations, advertisements, or links to
    other articles. The fetched webpage content is the evidence
    that should be provided to the LLM.
    """

    return {
        "source_number": source_number,
        "title": result.title,
        "url": result.url,
        "source": result.source,
        "published_at": (
            result.published_at.isoformat()
            if result.published_at
            else None
        ),
        "content": content,
    }


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

    If the initial search produces results that do not appear to
    mention the requested company/entity, the tool automatically
    retries using a focused entity query.

    Each successfully retrieved webpage is returned as a separate,
    explicitly identified research source.

    Search-result descriptions are not returned to the LLM because
    they may contain unrelated recommendation or navigation text.
    """

    provider = get_web_search_provider()
    search_service = WebSearchService(provider)

    research_timestamp = datetime.now(timezone.utc).isoformat()

    # -------------------------------------------------------------
    # Initial search
    # -------------------------------------------------------------

    search_result = search_service.search(
        query=query,
        topic=topic,
        days=days,
    )

    entity_query = _extract_entity_query(query)

    relevant_results = [
        result
        for result in search_result.results
        if _contains_entity(
            result,
            entity_query,
        )
    ]

    # -------------------------------------------------------------
    # Fallback search
    # -------------------------------------------------------------

    if (
        entity_query
        and not relevant_results
        and entity_query.lower() != query.strip().lower()
    ):
        print(
            f"No relevant results found for '{query}'. "
            f"Retrying focused search for '{entity_query}'."
        )

        search_result = search_service.search(
            query=entity_query,
            topic=topic,
            days=days,
        )

    # -------------------------------------------------------------
    # Rank the final search results
    # -------------------------------------------------------------

    ranked_results = rank_search_results(
        results=search_result.results,
        query=search_result.query,
        topic=topic,
    )

    # -------------------------------------------------------------
    # Fetch the most relevant pages
    # -------------------------------------------------------------

    page_fetcher = WebPageFetcher()

    research_results = []

    for result in ranked_results:
        try:
            content = page_fetcher.fetch(result.url)

            research_results.append(
                _build_source(
                    source_number=len(research_results) + 1,
                    result=result,
                    content=content,
                )
            )

        except Exception as exc:
            print(
                f"Failed to fetch {result.url}: {exc}"
            )
            continue

        # Keep the current two-source research design.
        if len(research_results) >= 2:
            break

    return {
        "research_timestamp": research_timestamp,
        "query": search_result.query,
        "topic": topic,
        "freshness_days": days,
        "sources": research_results,
    }