from abc import ABC, abstractmethod

from app.web.schemas import WebSearchResponse


class WebSearchProvider(ABC):
    @abstractmethod
    def search(
        self,
        query: str,
        topic: str = "general",
        days: int | None = None,
    ) -> WebSearchResponse:
        pass