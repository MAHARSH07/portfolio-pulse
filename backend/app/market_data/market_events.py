import re
from datetime import datetime, timezone

from app.web.providers.factory import get_web_search_provider
from app.web.schemas import WebSearchResult
from app.web.service import WebSearchService


ECONOMIC_EVENT_QUERIES = [
    {
        "query": (
            "RBI MPC October 2026 meeting scheduled dates "
            "October 5 7 2026"
        ),
        "country": "India",
        "category": "Indian Economy",
    },
    {
        "query": (
            "India CPI inflation release October 2026 "
            "scheduled date"
        ),
        "country": "India",
        "category": "Indian Economy",
    },
    {
        "query": (
            "India GDP release October November 2026 "
            "scheduled date"
        ),
        "country": "India",
        "category": "Indian Economy",
    },
    {
        "query": (
            "Federal Reserve FOMC meeting October 2026 "
            "scheduled date"
        ),
        "country": "United States",
        "category": "US Economy",
    },
    {
        "query": (
            "US CPI inflation October 2026 "
            "release date scheduled"
        ),
        "country": "United States",
        "category": "US Economy",
    },
    {
        "query": (
            "US jobs employment report October 2026 "
            "release date scheduled"
        ),
        "country": "United States",
        "category": "US Economy",
    },
    {
        "query": (
            "US GDP release October November 2026 "
            "scheduled date"
        ),
        "country": "United States",
        "category": "US Economy",
    },
]


PREFERRED_SOURCES = {
    "reuters.com": 5,
    "economictimes.com": 4,
    "m.economictimes.com": 4,
    "moneycontrol.com": 4,
    "business-standard.com": 4,
    "livemint.com": 4,
    "cnbc.com": 4,
    "federalreserve.gov": 5,
    "rbi.org.in": 5,
    "bls.gov": 5,
    "bea.gov": 5,
    "mospi.gov.in": 5,
}


MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


def _source_score(source: str | None) -> int:
    if not source:
        return 0

    return PREFERRED_SOURCES.get(
        source.lower(),
        0,
    )


def _freshness_score(
    published_at: datetime | None,
) -> int:
    if published_at is None:
        return 0

    if published_at.tzinfo is None:
        published_at = published_at.replace(
            tzinfo=timezone.utc
        )

    age_days = (
        datetime.now(timezone.utc) - published_at
    ).days

    if age_days <= 1:
        return 5

    if age_days <= 3:
        return 3

    if age_days <= 7:
        return 1

    return 0


def _parse_date(
    month: str,
    day: str,
    year: str | None,
) -> datetime | None:
    month_number = MONTHS.get(
        month.lower()
    )

    if month_number is None:
        return None

    current_year = datetime.now(
        timezone.utc
    ).year

    try:
        parsed_year = (
            int(year)
            if year is not None
            else current_year
        )

        return datetime(
            parsed_year,
            month_number,
            int(day),
            tzinfo=timezone.utc,
        )

    except ValueError:
        return None


def _extract_event_dates(
    text: str,
) -> tuple[
    datetime | None,
    datetime | None,
]:

    if not text:
        return None, None

    normalized = re.sub(
        r"\s+",
        " ",
        text,
    )

    # Examples:
    #
    # scheduled for October 5 to 7
    # scheduled to be held from October 5 to 7
    # scheduled from October 5 to October 7
    range_match = re.search(
        r"(?:"
        r"scheduled\s+to\s+be\s+held"
        r"|scheduled"
        r")?"
        r"\s*(?:from\s+)?"
        r"(January|February|March|April|May|June|July|August|"
        r"September|October|November|December)"
        r"\s+(\d{1,2})"
        r"(?:st|nd|rd|th)?"
        r"\s*(?:to|-|through)\s*"
        r"(?:(January|February|March|April|May|June|July|August|"
        r"September|October|November|December)\s+)?"
        r"(\d{1,2})"
        r"(?:st|nd|rd|th)?"
        r"(?:,?\s*(20\d{2}))?",
        normalized,
        re.IGNORECASE,
    )

    if range_match:
        start_month = range_match.group(1)
        start_day = range_match.group(2)

        end_month = (
            range_match.group(3)
            or start_month
        )

        end_day = range_match.group(4)
        year = range_match.group(5)

        start_date = _parse_date(
            start_month,
            start_day,
            year,
        )

        end_date = _parse_date(
            end_month,
            end_day,
            year,
        )

        if start_date and end_date:
            return start_date, end_date

    # Examples:
    #
    # scheduled for October 8
    # scheduled on October 8
    # will meet on October 28
    # release is scheduled for October 14
    # due on October 14
    # expected on October 14
    single_match = re.search(
        r"(?:"
        r"scheduled\s+(?:for|on)"
        r"|will\s+(?:meet|occur)\s+on"
        r"|meeting\s+(?:is\s+)?on"
        r"|release\s+is\s+scheduled\s+(?:for|on)"
        r"|release\s+date\s+is\s+"
        r"(?:scheduled\s+)?(?:for|on)"
        r"|due\s+on"
        r"|expected\s+on"
        r")\s+"
        r"(January|February|March|April|May|June|July|August|"
        r"September|October|November|December)"
        r"\s+(\d{1,2})"
        r"(?:st|nd|rd|th)?"
        r"(?:,?\s*(20\d{2}))?",
        normalized,
        re.IGNORECASE,
    )

    if single_match:
        event_date = _parse_date(
            single_match.group(1),
            single_match.group(2),
            single_match.group(3),
        )

        return event_date, None

    return None, None


def _detect_event_title(
    text: str,
) -> str | None:

    normalized = re.sub(
        r"\s+",
        " ",
        text,
    )

    # -------------------------
    # India
    # -------------------------

    if re.search(
        r"\bRBI\b.{0,100}\bMPC\b"
        r"|\bMPC\b.{0,100}\bRBI\b",
        normalized,
        re.IGNORECASE,
    ):
        return (
            "RBI Monetary Policy Committee Meeting"
        )

    if re.search(
        r"\bRBI\b.{0,100}"
        r"(?:policy meeting|monetary policy)",
        normalized,
        re.IGNORECASE,
    ):
        return "RBI Monetary Policy Meeting"

    if re.search(
        r"\bIndia\b.{0,80}\bCPI\b"
        r"|\bCPI\b.{0,80}\bIndia\b",
        normalized,
        re.IGNORECASE,
    ):
        return "India CPI Inflation Release"

    if re.search(
        r"\bIndia\b.{0,80}\bGDP\b"
        r"|\bGDP\b.{0,80}\bIndia\b",
        normalized,
        re.IGNORECASE,
    ):
        return "India GDP Release"

    # -------------------------
    # United States
    # -------------------------

    if re.search(
        r"\bFed\b"
        r"|\bFederal Reserve\b"
        r"|\bFOMC\b",
        normalized,
        re.IGNORECASE,
    ):
        return (
            "US Federal Reserve / FOMC Meeting"
        )

    if re.search(
        r"\bUS\b.{0,80}\bCPI\b"
        r"|\bCPI\b.{0,80}\bUS\b",
        normalized,
        re.IGNORECASE,
    ):
        return "US CPI Inflation Release"

    if re.search(
        r"\bUS\b.{0,100}"
        r"(?:jobs report|employment report|"
        r"nonfarm payrolls)",
        normalized,
        re.IGNORECASE,
    ):
        return "US Employment Report"

    if re.search(
        r"\bUS\b.{0,80}\bGDP\b"
        r"|\bGDP\b.{0,80}\bUS\b",
        normalized,
        re.IGNORECASE,
    ):
        return "US GDP Release"

    return None


def _event_identity(
    title: str,
) -> str:

    normalized = title.lower()

    normalized = re.sub(
        r"[^a-z0-9]+",
        " ",
        normalized,
    )

    normalized = re.sub(
        r"\bcommittee\b",
        "",
        normalized,
    )

    normalized = re.sub(
        r"\s+",
        " ",
        normalized,
    ).strip()

    return normalized


def _rank_results(
    results: list[WebSearchResult],
) -> list[WebSearchResult]:

    def score(
        result: WebSearchResult,
    ) -> int:

        value = 0

        value += _source_score(
            result.source
        )

        value += _freshness_score(
            result.published_at
        )

        if result.published_at is not None:
            value += 2

        return value

    return sorted(
        results,
        key=score,
        reverse=True,
    )


def _build_event(
    result: WebSearchResult,
    country: str,
    category: str,
) -> dict | None:

    text = " ".join(
        value
        for value in [
            result.title,
            result.description,
        ]
        if value
    )

    event_title = _detect_event_title(
        text
    )

    if event_title is None:
        return None

    event_date, end_date = (
        _extract_event_dates(text)
    )

    if event_date is None:
        return None

    now = datetime.now(
        timezone.utc
    )

    if end_date and end_date < now:
        status = "past"

    elif event_date <= now and (
        end_date is None
        or now <= end_date
    ):
        status = "ongoing"

    else:
        status = "upcoming"

    return {
        "title": event_title,
        "country": country,
        "category": category,
        "event_date": event_date,
        "end_date": end_date,
        "description": result.description,
        "source": result.source,
        "url": result.url,
        "status": status,
    }


def _deduplicate_events(
    events: list[dict],
) -> list[dict]:

    unique_events: dict[
        tuple[str, str, datetime],
        dict,
    ] = {}

    for event in events:

        identity = _event_identity(
            event["title"]
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

        existing_score = _source_score(
            existing["source"]
        )

        new_score = _source_score(
            event["source"]
        )

        if new_score > existing_score:
            unique_events[key] = event

    return sorted(
        unique_events.values(),
        key=lambda event: event[
            "event_date"
        ],
    )


class MarketEconomicEventsProvider:

    def __init__(self):
        provider = (
            get_web_search_provider()
        )

        self.search_service = (
            WebSearchService(provider)
        )

    def get_upcoming_events(
        self,
        days: int = 60,
    ) -> list[dict]:

        events = []

        for event_query in (
            ECONOMIC_EVENT_QUERIES
        ):

            search_result = (
                self.search_service.search(
                    query=event_query["query"],
                    topic="news",
                    days=days,
                )
            )

            ranked_results = (
                _rank_results(
                    search_result.results
                )
            )

            for result in ranked_results:

                event = _build_event(
                    result=result,
                    country=event_query[
                        "country"
                    ],
                    category=event_query[
                        "category"
                    ],
                )

                if event is not None:
                    events.append(event)

        deduplicated = (
            _deduplicate_events(events)
        )

        # The endpoint is an upcoming/ongoing
        # calendar, so don't return events that
        # have already completely finished.
        now = datetime.now(
            timezone.utc
        )

        return [
            event
            for event in deduplicated
            if (
                event["end_date"] is None
                and event["event_date"] >= now
            )
            or (
                event["end_date"] is not None
                and event["end_date"] >= now
            )
            or event["status"] == "ongoing"
        ]