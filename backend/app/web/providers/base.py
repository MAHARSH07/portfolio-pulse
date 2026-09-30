from abc import ABC, abstractmethod

from app.web.schemas import WebSearchResponse


class WebSearchProvider(ABC):
    @abstractmethod
    def search(self, query: str) -> WebSearchResponse:
        pass