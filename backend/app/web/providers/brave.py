import httpx

from app.core.config import settings
from app.web.providers.base import WebSearchProvider
from app.web.schemas import WebSearchResponse, WebSearchResult


class BraveSearchProvider(WebSearchProvider):
    BASE_URL = "https://api.search.brave.com/res/v1/web/search"

    def search(
        self,
        query: str,
        topic: str = "general",
        days: int | None = None,
    ) -> WebSearchResponse:
        if not settings.brave_search_api_key:
            raise RuntimeError("BRAVE_SEARCH_API_KEY is not configured.")

        response = httpx.get(
            self.BASE_URL,
            headers={
                "Accept": "application/json",
                "X-Subscription-Token": settings.brave_search_api_key,
            },
            params={
                "q": query,
                "country": "IN",
                "search_lang": "en",
                "count": 10,
            },
            timeout=20.0,
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for item in data.get("web", {}).get("results", []):
            results.append(
                WebSearchResult(
                    title=item["title"],
                    url=item["url"],
                    description=item.get("description"),
                    source=item.get("profile", {}).get("long_name"),
                )
            )

        return WebSearchResponse(
            query=query,
            results=results,
        )
