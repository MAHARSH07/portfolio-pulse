import re
from datetime import datetime, timezone

import httpx
from bs4 import BeautifulSoup

from app.market_data.event_sources.base import (
    EconomicEventSource,
    calculate_event_status,
)
from app.schemas.market import MarketEconomicEvent


class RBIEventSource(EconomicEventSource):

    URL = (
        "https://www.rbi.org.in/"
        "Scripts/BS_PressReleaseDisplay.aspx"
        "?prid=62422"
    )

    MONTHS = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }

    def get_events(
        self,
    ) -> list[MarketEconomicEvent]:

        response = httpx.get(
            self.URL,
            timeout=20.0,
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        text = soup.get_text(
            " ",
            strip=True,
        )

        schedule_match = re.search(
            r"Dates of meetings of Monetary Policy "
            r"Committee for 2026-27"
            r"(.*?)"
            r"\(Brij Raj\)",
            text,
            flags=re.IGNORECASE,
        )

        if not schedule_match:
            raise RuntimeError(
                "Could not locate the RBI 2026-27 MPC schedule "
                "in the official RBI page."
            )

        schedule_text = schedule_match.group(1)

        pattern = re.compile(
            r"(January|February|March|April|May|June|July|"
            r"August|September|October|November|December)"
            r"\s+"
            r"(\d{1,2}),\s+"
            r"(\d{1,2})\s+and\s+"
            r"(\d{1,2}),\s+"
            r"(\d{4})",
            flags=re.IGNORECASE,
        )

        events: list[MarketEconomicEvent] = []

        for match in pattern.finditer(schedule_text):
            month_name = match.group(1).capitalize()
            first_day = int(match.group(2))
            second_day = int(match.group(3))
            third_day = int(match.group(4))
            year = int(match.group(5))

            month = self.MONTHS[month_name]

            start_date = datetime(
                year,
                month,
                first_day,
                tzinfo=timezone.utc,
            )

            end_date = datetime(
                year,
                month,
                third_day,
                tzinfo=timezone.utc,
            )

            description = (
                f"Reserve Bank of India's Monetary Policy "
                f"Committee meeting scheduled for "
                f"{month_name} {first_day}–{third_day}, "
                f"{year}."
            )

            events.append(
                MarketEconomicEvent(
                    title="RBI Monetary Policy Committee Meeting",
                    country="India",
                    category="Central Bank",
                    event_date=start_date,
                    end_date=end_date,
                    description=description,
                    source="rbi.org.in",
                    url=self.URL,
                    status=calculate_event_status(
                        start_date,
                        end_date,
                    ),
                )
            )

        return events