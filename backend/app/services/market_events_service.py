from app.market_data.market_events import (
    MarketEconomicEventsProvider,
)
from app.schemas.market import (
    MarketEconomicEvent,
    MarketEconomicEventsResponse,
)


def get_market_events() -> MarketEconomicEventsResponse:
    provider = MarketEconomicEventsProvider()

    events = provider.get_upcoming_events()

    return MarketEconomicEventsResponse(
        events=[
            MarketEconomicEvent(**event)
            for event in events
        ]
    )