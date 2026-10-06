from datetime import datetime, timezone

from app.market_data.event_sources.bea import BEAEventSource
from app.market_data.event_sources.fed import FedEventSource
from app.market_data.event_sources.mospi import MoSPIEventSource
from app.market_data.event_sources.rbi import RBIEventSource


class MarketEconomicEventsProvider:

    def __init__(self):
        self.sources = [
            RBIEventSource(),
            FedEventSource(),
            BEAEventSource(),
            MoSPIEventSource(),
        ]

    def get_upcoming_events(
        self,
        days: int = 60,
    ) -> list[dict]:

        now = datetime.now(timezone.utc)

        events = []

        for source in self.sources:
            source_events = source.get_events()

            for event in source_events:
                events.append(
                    event.model_dump()
                )

        events = self._deduplicate_events(
            events
        )

        from datetime import timedelta

        upcoming_events = []

        cutoff_date = now + timedelta(days=days)

        for event in events:
            event_date = event["event_date"]
            end_date = event["end_date"]

            effective_end_date = (
                end_date
                if end_date is not None
                else event_date
            )

            # Completely finished events
            if effective_end_date < now:
                continue

            # Events starting beyond the requested window
            if event_date > cutoff_date:
                continue

            upcoming_events.append(event)

        upcoming_events.sort(
            key=lambda event: event["event_date"]
        )

        return upcoming_events

    @staticmethod
    def _deduplicate_events(
        events: list[dict],
    ) -> list[dict]:

        unique_events = {}

        for event in events:

            identity = (
                event["title"]
                .strip()
                .lower()
            )

            key = (
                identity,
                event["country"],
                event["event_date"],
            )

            existing = unique_events.get(
                key
            )

            if existing is None:
                unique_events[key] = event
                continue

            # Prefer the event that has a
            # description and a more specific URL.
            existing_description = (
                existing.get("description")
            )

            new_description = (
                event.get("description")
            )

            if (
                not existing_description
                and new_description
            ):
                unique_events[key] = event

        return list(
            unique_events.values()
        )