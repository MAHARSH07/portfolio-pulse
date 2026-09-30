from app.web.providers.base import WebSearchProvider
from app.web.schemas import WebSearchResponse


class WebSearchService:
    def __init__(self, provider: WebSearchProvider):
        self.provider = provider

    def search(
        self,
        query: str,
        topic: str = "general",
        days: int | None = None,
    ) -> WebSearchResponse:
        return self.provider.search(
            query=query,
            topic=topic,
            days=days,
        )
