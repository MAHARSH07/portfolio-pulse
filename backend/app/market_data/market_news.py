from datetime import datetime, timezone

from app.web.providers.factory import get_web_search_provider
from app.web.schemas import WebSearchResult
from app.web.service import WebSearchService


MARKET_NEWS_QUERIES = [
    {
        "query": "Indian stock market latest news NIFTY Sensex",
        "category": "Indian Markets",
    },
    {
        "query": "global stock market latest news S&P 500 NASDAQ",
        "category": "Global Markets",
    },
    {
        "query": "gold silver latest market news",
        "category": "Commodities",
    },
]


PREFERRED_SOURCES = {
    "reuters.com": 5,
    "economictimes.com": 4,
    "m.economictimes.com": 4,
    "moneycontrol.com": 4,
    "business-standard.com": 4,
    "ndtvprofit.com": 4,
    "livemint.com": 4,
}


def _source_score(source: str | None) -> int:
    if not source:
        return 0

    return PREFERRED_SOURCES.get(
        source.lower(),
        0,
    )


def _freshness_score(
    published_at: datetime | None,
) -> int:
    if published_at is None:
        return 0

    if published_at.tzinfo is None:
        published_at = published_at.replace(
            tzinfo=timezone.utc
        )

    age_days = (
        datetime.now(timezone.utc) - published_at
    ).days

    if age_days <= 1:
        return 5

    if age_days <= 3:
        return 3

    if age_days <= 7:
        return 1

    return 0


def _rank_market_news(
    results: list[WebSearchResult],
) -> list[WebSearchResult]:

    def score(result: WebSearchResult) -> int:
        score = 0

        score += _source_score(result.source)

        score += _freshness_score(
            result.published_at
        )

        if result.published_at is not None:
            score += 2

        return score

    return sorted(
        results,
        key=score,
        reverse=True,
    )


class MarketNewsProvider:

    def __init__(self):
        provider = get_web_search_provider()

        self.search_service = WebSearchService(
            provider
        )

    def get_latest_news(
        self,
        days: int = 7,
        results_per_category: int = 4,
    ) -> list[dict]:

        articles = []

        for market_query in MARKET_NEWS_QUERIES:

            search_result = self.search_service.search(
                query=market_query["query"],
                topic="news",
                days=days,
            )

            ranked_results = _rank_market_news(
                search_result.results
            )

            selected_results = ranked_results[
                :results_per_category
            ]

            for result in selected_results:
                articles.append(
                    {
                        "title": result.title,
                        "url": result.url,
                        "description": result.description,
                        "published_at": result.published_at,
                        "source": result.source,
                        "category": market_query["category"],
                    }
                )

        return articles