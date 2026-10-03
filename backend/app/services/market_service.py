from app.market_data.market_overview import MarketOverviewProvider
from app.schemas.market import MarketOverview


def get_market_overview() -> MarketOverview:
    provider = MarketOverviewProvider()

    instruments = provider.get_market_overview()

    return MarketOverview(
        instruments=instruments
    )