from datetime import datetime

from pydantic import BaseModel


class WebSearchResult(BaseModel):
    title: str
    url: str
    description: str | None = None
    published_at: datetime | None = None
    source: str | None = None


class WebSearchResponse(BaseModel):
    query: str
    results: list[WebSearchResult]