import re
from datetime import datetime, time
from zoneinfo import ZoneInfo

import httpx
from bs4 import BeautifulSoup

from app.market_data.event_sources.base import (
    EconomicEventSource,
    calculate_event_status,
)
from app.schemas.market import MarketEconomicEvent


class MoSPIEventSource(EconomicEventSource):

    URL = (
        "https://www.mospi.gov.in/api/"
        "release-calender/fetch-all-release-calender-Web"
    )

    INDIA_TIMEZONE = ZoneInfo(
        "Asia/Kolkata"
    )

    PAGE_SIZE = 20

    def get_events(
        self,
    ) -> list[MarketEconomicEvent]:

        events: list[MarketEconomicEvent] = []

        page = 1

        while True:
            payload = {
                "lang": "en",
                "page": page,
                "limit": self.PAGE_SIZE,
                "year": datetime.now(
                    self.INDIA_TIMEZONE
                ).year,
            }

            response = httpx.post(
                self.URL,
                json=payload,
                timeout=20.0,
            )

            response.raise_for_status()

            data = response.json()

            if not data.get("success"):
                raise RuntimeError(
                    "MoSPI release calendar API returned "
                    "an unsuccessful response."
                )

            page_data = data.get("data", [])
            pagination = data.get(
                "pagination",
                {},
            )

            for item in page_data:
                event = self._parse_event(item)

                if event is not None:
                    events.append(event)

            total_pages = pagination.get(
                "totalPages",
                page,
            )

            if page >= total_pages:
                break

            page += 1

        return events

    def _parse_event(
        self,
        item: dict,
    ) -> MarketEconomicEvent | None:

        title = self._clean_text(
            item.get("title")
        )

        year = item.get("year")
        month = item.get("month")
        day = item.get("day")

        if (
            not title
            or not isinstance(year, int)
            or not isinstance(month, int)
            or not isinstance(day, int)
        ):
            return None

        try:
            start_date = datetime(
                year,
                month,
                day,
                0,
                0,
                tzinfo=self.INDIA_TIMEZONE,
            )

            end_date = datetime(
                year,
                month,
                day,
                23,
                59,
                59,
                tzinfo=self.INDIA_TIMEZONE,
            )

        except ValueError:
            return None

        description = self._clean_text(
            item.get("description")
        )

        doc_url = item.get("doc_url")

        source_url = self._build_document_url(
            doc_url
        )

        if source_url is None:
            source_url = (
                "https://www.mospi.gov.in/"
                "release-calendar"
            )

        return MarketEconomicEvent(
            title=title,
            country="India",
            category="Economic Data",
            event_date=start_date,
            end_date=end_date,
            description=description,
            source="mospi.gov.in",
            url=source_url,
            status=calculate_event_status(
                start_date,
                end_date,
            ),
        )

    @staticmethod
    def _clean_text(
        value: str | None,
    ) -> str | None:

        if not value:
            return None

        text = BeautifulSoup(
            value,
            "html.parser",
        ).get_text(
            " ",
            strip=True,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip() or None

    @staticmethod
    def _build_document_url(
        doc_url: str | None,
    ) -> str | None:

        if not doc_url:
            return None

        if doc_url.startswith(
            "http://"
        ) or doc_url.startswith(
            "https://"
        ):
            return doc_url

        return (
            "https://www.mospi.gov.in/"
            + doc_url.lstrip("/")
        )