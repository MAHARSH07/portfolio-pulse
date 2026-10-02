from datetime import datetime, timezone

from app.web.schemas import WebSearchResult


# Sources that are generally useful for financial/company research.
PREFERRED_SOURCES = {
    "reuters.com": 5,
    "economictimes.com": 4,
    "m.economictimes.com": 4,
    "moneycontrol.com": 4,
    "business-standard.com": 4,
    "ndtvprofit.com": 4,
    "livemint.com": 4,
}


def rank_search_results(
    results: list[WebSearchResult],
    query: str,
    topic: str = "general",
) -> list[WebSearchResult]:
    query_terms = {
        term.lower()
        for term in query.split()
        if len(term) > 2
    }

    def score(result: WebSearchResult) -> int:
        score = 0

        title = result.title.lower()
        description = (result.description or "").lower()
        source = (result.source or "").lower()

        # Exact query/company terms appearing in the title.
        for term in query_terms:
            if term in title:
                score += 3
            elif term in description:
                score += 1

        # Prefer known financial/news sources.
        score += PREFERRED_SOURCES.get(source, 0)

        # For news searches, prefer results with a publication date.
        if topic == "news" and result.published_at is not None:
            score += 3

            if result.published_at.tzinfo is None:
                published_at = result.published_at.replace(
                    tzinfo=timezone.utc
                )
            else:
                published_at = result.published_at

            age_days = (
                datetime.now(timezone.utc) - published_at
            ).days

            if age_days <= 1:
                score += 5
            elif age_days <= 3:
                score += 3
            elif age_days <= 7:
                score += 1

        return score

    return sorted(
        results,
        key=score,
        reverse=True,
    )