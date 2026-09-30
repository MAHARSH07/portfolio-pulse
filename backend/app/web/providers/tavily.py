import httpx

from app.core.config import settings
from app.web.providers.base import WebSearchProvider
from app.web.schemas import WebSearchResponse, WebSearchResult
from urllib.parse import urlparse


class TavilySearchProvider(WebSearchProvider):
    BASE_URL = "https://api.tavily.com/search"

    @staticmethod
    def _get_source(url: str) -> str | None:
        hostname = urlparse(url).hostname

        if hostname is None:
            return None

        return hostname.removeprefix("www.")

    def search(self, query: str) -> WebSearchResponse:
        if not settings.tavily_api_key:
            raise RuntimeError("TAVILY_API_KEY is not configured.")

        response = httpx.post(
            self.BASE_URL,
            headers={
                "Authorization": f"Bearer {settings.tavily_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "query": query,
                "search_depth": "basic",
                "max_results": 10,
                "country": "india",
            },
            timeout=20.0,
        )

        response.raise_for_status()

        data = response.json()

        results = [
            WebSearchResult(
                title=item["title"],
                url=item["url"],
                description=item.get("content"),
                source=self._get_source(item["url"]),
            )
            for item in data.get("results", [])
        ]

        return WebSearchResponse(
            query=query,
            results=results,
        )
