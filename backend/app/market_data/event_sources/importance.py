import re

from app.schemas.market import EventImportance, MarketEconomicEvent


HIGH_IMPORTANCE_PATTERNS = [
    r"\bmonetary policy committee\b",
    r"\bmpc meeting\b",
    r"\bfomc\b",
    r"\bfederal reserve\b",
    r"\binterest rate decision\b",
    r"\bconsumer price index\b",
    r"\bcpi\b",
    r"\binflation release\b",
    r"\bgdp\s*\(\s*advance estimate\s*\)",
    r"\bgdp\s*\(\s*second estimate\s*\)",
    r"\bgross domestic product\b",
]

MEDIUM_IMPORTANCE_PATTERNS = [
    r"\bindustrial production\b",
    r"\biip\b",
    r"\bemployment report\b",
    r"\bjobs report\b",
    r"\bnonfarm payrolls\b",
    r"\bperiodic labour force survey\b",
    r"\bunemployment\b",
    r"\binternational trade\b",
    r"\btrade in goods and services\b",
    r"\bpersonal income and outlays\b",
    r"\bproducer price index\b",
    r"\bppi\b",
]


# Specific releases that should not be rated high merely because
# their title contains the term GDP.
LOW_IMPORTANCE_PATTERNS = [
    r"\bgdp\b.*\b(county|state|regional)\b",
]


def classify_event_importance(
    event: MarketEconomicEvent,
) -> EventImportance:
    title = event.title.lower()

    # Apply specific exceptions before broader rules.
    if any(
        re.search(pattern, title)
        for pattern in LOW_IMPORTANCE_PATTERNS
    ):
        return "low"

    if any(
        re.search(pattern, title)
        for pattern in HIGH_IMPORTANCE_PATTERNS
    ):
        return "high"

    text = " ".join(
        value
        for value in [
            event.title,
            event.category,
            event.description or "",
        ]
        if value
    ).lower()

    if any(
        re.search(pattern, text)
        for pattern in MEDIUM_IMPORTANCE_PATTERNS
    ):
        return "medium"

    return "low"


def get_event_market_impact(
    event: MarketEconomicEvent,
) -> str:
    """Return deterministic context about a potential market impact."""

    text = " ".join(
        value
        for value in [
            event.title,
            event.category,
            event.description or "",
        ]
        if value
    ).lower()

    if any(
        term in text
        for term in [
            "monetary policy committee",
            "mpc meeting",
            "rbi",
        ]
    ):
        return (
            "May influence Indian interest-rate expectations, "
            "banking stocks, bond yields, the rupee, and gold. "
            "The impact depends on the policy decision and guidance "
            "relative to market expectations."
        )

    if any(
        term in text
        for term in [
            "fomc",
            "federal reserve",
            "interest rate decision",
        ]
    ):
        return (
            "May influence US Treasury yields, the US dollar, "
            "global equities, and gold and silver. Changes in rate "
            "expectations can also affect emerging markets, including "
            "India. The reaction depends on the decision and guidance "
            "relative to expectations."
        )

    if any(
        term in text
        for term in [
            "consumer price index",
            "inflation release",
            "cpi",
            "producer price index",
            "ppi",
        ]
    ):
        return (
            "Inflation data may shift expectations for future interest "
            "rates, affecting bond yields, currencies, equities, and "
            "precious metals. Compare the reported figure with forecasts "
            "and the previous reading."
        )

    if any(
        term in text
        for term in [
            "gdp (advance estimate)",
            "gdp (second estimate)",
            "gross domestic product",
        ]
    ):
        return (
            "GDP data provides a signal about economic growth and may "
            "influence earnings expectations, interest-rate outlooks, "
            "bond yields, and equity markets. Compare the release with "
            "forecasts and earlier estimates."
        )

    if any(
        term in text
        for term in [
            "industrial production",
            "iip",
        ]
    ):
        return (
            "Industrial production data can provide clues about "
            "manufacturing and economic momentum, potentially affecting "
            "cyclical stocks and growth expectations. Compare the result "
            "with forecasts and previous readings."
        )

    if any(
        term in text
        for term in [
            "employment report",
            "jobs report",
            "nonfarm payrolls",
            "unemployment",
            "periodic labour force survey",
        ]
    ):
        return (
            "Employment data can influence assessments of economic "
            "strength, wage pressure, and future interest rates, with "
            "possible effects on equities, bonds, and currencies."
        )

    if any(
        term in text
        for term in [
            "international trade",
            "trade in goods and services",
        ]
    ):
        return (
            "Trade data can provide clues about export demand, imports, "
            "and economic momentum. It may affect currency expectations "
            "and trade-sensitive industries, depending on the result "
            "and market expectations."
        )

    if "personal income and outlays" in text:
        return (
            "Personal income and spending data can indicate household "
            "financial health and consumer demand. The figures may also "
            "influence inflation and interest-rate expectations."
        )

    return (
        "The direct market impact is uncertain. Check the release details, "
        "compare them with market expectations, and assess whether the "
        "event is relevant to the assets you follow."
    )