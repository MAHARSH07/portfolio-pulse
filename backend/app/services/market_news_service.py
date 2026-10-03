from app.market_data.market_news import MarketNewsProvider
from app.schemas.market import (
    MarketNewsArticle,
    MarketNewsResponse,
)


def get_market_news() -> MarketNewsResponse:
    provider = MarketNewsProvider()

    articles = provider.get_latest_news()

    return MarketNewsResponse(
        articles=[
            MarketNewsArticle(**article)
            for article in articles
        ]
    )