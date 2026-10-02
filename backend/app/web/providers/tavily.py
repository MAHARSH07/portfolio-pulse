from datetime import datetime
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse

import httpx

from app.core.config import settings
from app.web.providers.base import WebSearchProvider
from app.web.schemas import WebSearchResponse, WebSearchResult


class TavilySearchProvider(WebSearchProvider):
    BASE_URL = "https://api.tavily.com/search"

    @staticmethod
    def _get_source(url: str) -> str | None:
        hostname = urlparse(url).hostname

        if hostname is None:
            return None

        return hostname.removeprefix("www.")

    @staticmethod
    def _parse_published_at(value: str | None) -> datetime | None:
        if not value:
            return None

        try:
            return parsedate_to_datetime(value)
        except (TypeError, ValueError):
            return None

    def search(
        self,
        query: str,
        topic: str = "general",
        days: int | None = None,
    ) -> WebSearchResponse:
        if not settings.tavily_api_key:
            raise RuntimeError("TAVILY_API_KEY is not configured.")

        payload = {
            "query": query,
            "search_depth": "basic",
            "max_results": 5,
            "country": "india",
            "topic": topic,
        }

        if days is not None:
            payload["days"] = days

        response = httpx.post(
            self.BASE_URL,
            headers={
                "Authorization": f"Bearer {settings.tavily_api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=20.0,
        )

        response.raise_for_status()

        data = response.json()

        results = [
            WebSearchResult(
                title=item["title"],
                url=item["url"],
                description=(item.get("content") or "")[:1000],
                source=self._get_source(item["url"]),
                published_at=self._parse_published_at(
                    item.get("published_date")
                ),
            )
            for item in data.get("results", [])
        ]

        return WebSearchResponse(
            query=query,
            results=results,
        )