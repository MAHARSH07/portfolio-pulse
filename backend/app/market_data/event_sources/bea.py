from datetime import datetime
from zoneinfo import ZoneInfo

import httpx
from bs4 import BeautifulSoup

from app.market_data.event_sources.base import (
    EconomicEventSource,
    calculate_event_status,
)
from app.schemas.market import MarketEconomicEvent


class BEAEventSource(EconomicEventSource):

    URL = "https://www.bea.gov/news/schedule"

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

    EASTERN_TIMEZONE = ZoneInfo(
        "America/New_York"
    )

    UTC_TIMEZONE = ZoneInfo("UTC")

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

        schedule_table = soup.select_one(
            "#release-schedule-table"
        )

        if schedule_table is None:
            raise RuntimeError(
                "Could not locate the BEA release schedule "
                "table on the official BEA page."
            )

        events = []

        rows = schedule_table.select(
            "tbody tr"
        )

        for row in rows:
            event = self._parse_release(row)

            if event is not None:
                events.append(event)

        return events

    def _parse_release(
        self,
        row,
    ) -> MarketEconomicEvent | None:

        date_element = row.select_one(
            ".scheduled-date"
        )

        title_element = row.select_one(
            ".release-title"
        )

        if (
            date_element is None
            or title_element is None
        ):
            return None

        release_date_element = date_element.select_one(
            ".release-date"
        )

        time_element = date_element.find(
            "small"
        )

        if (
            release_date_element is None
            or time_element is None
        ):
            return None

        date_text = release_date_element.get_text(
            " ",
            strip=True,
        )

        time_text = time_element.get_text(
            " ",
            strip=True,
        )

        title = title_element.get_text(
            " ",
            strip=True,
        )

        if (
            not date_text
            or not time_text
            or not title
        ):
            return None

        date_parts = date_text.split()

        if len(date_parts) != 2:
            return None

        month_name = date_parts[0]
        day_text = date_parts[1]

        if month_name not in self.MONTHS:
            return None

        try:
            day = int(day_text)
        except ValueError:
            return None

        release_time = self._parse_release_time(
            time_text
        )

        if release_time is None:
            return None

        hour, minute = release_time

        month = self.MONTHS[month_name]

        eastern_datetime = datetime(
            2026,
            month,
            day,
            hour,
            minute,
            tzinfo=self.EASTERN_TIMEZONE,
        )

        event_date = eastern_datetime.astimezone(
            self.UTC_TIMEZONE
        )

        return MarketEconomicEvent(
            title=title,
            country="United States",
            category="Economic Data",
            event_date=event_date,
            end_date=event_date,
            description=(
                f"Scheduled BEA release at "
                f"{hour:02d}:{minute:02d} Eastern Time: "
                f"{title}."
            ),
            source="bea.gov",
            url=self.URL,
            status=calculate_event_status(
                event_date,
                event_date,
            ),
        )

    def _parse_release_time(
        self,
        time_text: str,
    ) -> tuple[int, int] | None:

        parts = time_text.split()

        if len(parts) != 2:
            return None

        time_value = parts[0]
        meridiem = parts[1].upper()

        time_parts = time_value.split(":")

        if len(time_parts) != 2:
            return None

        try:
            hour = int(time_parts[0])
            minute = int(time_parts[1])
        except ValueError:
            return None

        if meridiem not in {"AM", "PM"}:
            return None

        if hour < 1 or hour > 12:
            return None

        if minute < 0 or minute > 59:
            return None

        if meridiem == "AM":
            if hour == 12:
                hour = 0
        else:
            if hour != 12:
                hour += 12

        return hour, minute