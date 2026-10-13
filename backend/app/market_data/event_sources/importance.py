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


def classify_event_importance(
    event: MarketEconomicEvent,
) -> EventImportance:
    title = event.title.lower()

    # Classify specific GDP releases before applying general rules.
    if re.search(
        r"\bgdp\b.*\b(county|state|regional)\b",
        title,
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