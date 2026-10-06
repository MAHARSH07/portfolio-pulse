import re
from datetime import datetime, timezone

import httpx
from bs4 import BeautifulSoup

from app.market_data.event_sources.base import (
    EconomicEventSource,
    calculate_event_status,
)
from app.schemas.market import MarketEconomicEvent


class FedEventSource(EconomicEventSource):

    URL = (
        "https://www.federalreserve.gov/"
        "monetarypolicy/fomccalendars.htm"
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

        calendar_panel = self._get_2026_calendar(
            soup
        )

        if calendar_panel is None:
            raise RuntimeError(
                "Could not locate the 2026 FOMC calendar "
                "in the official Federal Reserve page."
            )

        events = []

        meetings = calendar_panel.select(
            ".fomc-meeting"
        )

        for meeting in meetings:
            event = self._parse_meeting(meeting)

            if event is not None:
                events.append(event)

        return events

    def _get_2026_calendar(
        self,
        soup: BeautifulSoup,
    ):
        """
        Locate the panel containing the 2026 FOMC meetings.
        """

        heading = soup.find(
            "a",
            string=re.compile(
                r"2026 FOMC Meetings",
                re.IGNORECASE,
            ),
        )

        if heading is None:
            return None

        panel = heading.find_parent(
            "div",
            class_="panel",
        )

        return panel

    def _parse_meeting(
        self,
        meeting,
    ) -> MarketEconomicEvent | None:
        """
        Parse one FOMC meeting row.
        """

        month_element = meeting.select_one(
            ".fomc-meeting__month"
        )

        date_element = meeting.select_one(
            ".fomc-meeting__date"
        )

        if (
            month_element is None
            or date_element is None
        ):
            return None

        month_name = month_element.get_text(
            " ",
            strip=True,
        )

        date_text = date_element.get_text(
            " ",
            strip=True,
        )

        month_name = month_name.rstrip("*").strip()
        date_text = date_text.rstrip("*").strip()

        if month_name not in self.MONTHS:
            return None

        date_match = re.fullmatch(
            r"(\d{1,2})(?:[-–](\d{1,2}))?",
            date_text,
        )

        if date_match is None:
            return None

        start_day = int(
            date_match.group(1)
        )

        end_day = (
            int(date_match.group(2))
            if date_match.group(2)
            else start_day
        )

        month = self.MONTHS[month_name]

        start_date = datetime(
            2026,
            month,
            start_day,
            tzinfo=timezone.utc,
        )

        end_date = datetime(
            2026,
            month,
            end_day,
            tzinfo=timezone.utc,
        )

        date_description = (
            f"{month_name} {start_day}"
        )

        if end_day != start_day:
            date_description += (
                f"–{end_day}"
            )

        date_description += ", 2026"

        return MarketEconomicEvent(
            title="US Federal Reserve / FOMC Meeting",
            country="United States",
            category="Central Bank",
            event_date=start_date,
            end_date=end_date,
            description=(
                "Federal Open Market Committee "
                f"meeting scheduled for "
                f"{date_description}."
            ),
            source="federalreserve.gov",
            url=self.URL,
            status=calculate_event_status(
                start_date,
                end_date,
            ),
        )