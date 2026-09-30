from app.core.config import settings
from app.web.providers.base import WebSearchProvider
from app.web.providers.brave import BraveSearchProvider
from app.web.providers.tavily import TavilySearchProvider


def get_web_search_provider() -> WebSearchProvider:
    provider = settings.web_search_provider.lower()

    if provider == "tavily":
        return TavilySearchProvider()

    if provider == "brave":
        return BraveSearchProvider()

    raise ValueError(
        f"Unsupported web search provider: {settings.web_search_provider}"
    )