from sqlalchemy.orm import Session

from app.market_data.market_events import (
    MarketEconomicEventsProvider,
)
from app.market_data.event_sources.portfolio_relevance import (
    get_portfolio_event_relevance,
)
from app.repositories.portfolio_repository import get_holdings
from app.schemas.market import (
    MarketEconomicEvent,
    MarketEconomicEventsResponse,
)


def get_market_events(
    db: Session,
) -> MarketEconomicEventsResponse:
    provider = MarketEconomicEventsProvider()

    events = provider.get_upcoming_events()

    holding_models = get_holdings(db)

    holdings = [
        {
            "symbol": holding.symbol,
            "company_name": holding.instrument.name,
        }
        for holding in holding_models
    ]

    enriched_events = []

    for event_data in events:
        event = MarketEconomicEvent(**event_data)

        relevance = get_portfolio_event_relevance(
            event=event,
            holdings=holdings,
        )

        enriched_event_data = event.model_dump()
        enriched_event_data["portfolio_relevance"] = relevance

        enriched_events.append(
            MarketEconomicEvent(**enriched_event_data)
        )

    return MarketEconomicEventsResponse(
        events=enriched_events
    )