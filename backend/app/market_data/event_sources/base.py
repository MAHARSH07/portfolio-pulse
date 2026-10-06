from abc import ABC, abstractmethod
from datetime import datetime, timezone

from app.schemas.market import MarketEconomicEvent


def calculate_event_status(
    event_date: datetime,
    end_date: datetime | None = None,
) -> str:
    """
    Calculate the current status of an economic event.

    upcoming  -> event has not started
    ongoing   -> event is currently happening
    completed -> event has finished
    """

    now = datetime.now(timezone.utc)

    if now < event_date:
        return "upcoming"

    effective_end_date = end_date or event_date

    if now <= effective_end_date:
        return "ongoing"

    return "completed"


class EconomicEventSource(ABC):

    @abstractmethod
    def get_events(self) -> list[MarketEconomicEvent]:
        """
        Fetch scheduled economic events from an
        authoritative source.
        """
        raise NotImplementedError