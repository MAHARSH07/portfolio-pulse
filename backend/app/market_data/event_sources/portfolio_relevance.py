
from app.market_data.event_sources.sector_mapping import (
    get_holding_sector,
)
from app.schemas.market import MarketEconomicEvent


EVENT_SECTOR_RULES = [
    {
        "id": "rbi_policy",
        "keywords": [
            "monetary policy committee",
            "mpc meeting",
            "reserve bank of india",
            "rbi monetary policy",
        ],
        "countries": {"india"},
        "sectors": {"banking", "financial_services"},
        "asset_classes": {"gold"},
        "reason": (
            "RBI policy can influence Indian interest rates, "
            "bank funding conditions, borrowing costs, and gold."
        ),
    },
    {
        "id": "fed_policy",
        "keywords": [
            "fomc",
            "federal reserve",
            "interest rate decision",
        ],
        "countries": {"united states"},
        "sectors": {
            "technology",
            "financial_services",
            "banking",
            "exporters",
        },
        "asset_classes": {
            "gold",
            "silver",
            "broad_market_equity",
            "midcap_equity",
        },
        "reason": (
            "US monetary policy can influence global liquidity, "
            "currency movements, international investor flows, "
            "equity markets, and precious metals."
        ),
    },
    {
        "id": "inflation",
        "keywords": [
            "consumer price index",
            "inflation release",
            "producer price index",
            "cpi",
            "ppi",
        ],
        "countries": {"india", "united states"},
        "sectors": {
            "consumer",
            "retail",
            "manufacturing",
            "financial_services",
            "banking",
        },
        "asset_classes": {
            "gold",
            "silver",
            "broad_market_equity",
            "midcap_equity",
        },
        "reason": (
            "Inflation data can influence interest-rate expectations, "
            "input costs, precious metals, and equity markets."
        ),
    },
    {
        "id": "gdp",
        "keywords": [
            "gdp (advance estimate)",
            "gdp (second estimate)",
            "gross domestic product",
        ],
        "countries": {"india", "united states"},
        "sectors": {
            "technology",
            "manufacturing",
            "financial_services",
            "banking",
            "industrials",
            "energy",
        },
        "asset_classes": {
            "broad_market_equity",
            "midcap_equity",
        },
        "reason": (
            "GDP data can influence economic-growth and earnings "
            "expectations and may affect broad equity markets. "
            "The actual market reaction depends on the result "
            "relative to expectations."
        ),
    },
    {
        "id": "trade",
        "keywords": [
            "international trade",
            "trade in goods and services",
        ],
        "countries": {"india", "united states"},
        "sectors": {
            "technology",
            "exporters",
            "manufacturing",
            "industrials",
        },
        "asset_classes": {
            "broad_market_equity",
            "midcap_equity",
        },
        "reason": (
            "Trade data can provide clues about export demand, "
            "currency movements, and global economic activity."
        ),
    },
    {
        "id": "personal_income",
        "keywords": [
            "personal income and outlays",
        ],
        "countries": {"united states"},
        "sectors": {
            "consumer",
            "retail",
        },
        "asset_classes": {
            "broad_market_equity",
            "midcap_equity",
        },
        "reason": (
            "Personal income and spending data can indicate consumer "
            "demand and may influence inflation expectations and "
            "broad equity markets."
        ),
    },
]


def get_portfolio_event_relevance(
    event: MarketEconomicEvent,
    holdings: list[dict],
) -> dict:
    """Match events to potential portfolio exposures using rules."""

    title = event.title.strip().lower()
    text = " ".join(
        value
        for value in [
            event.title,
            event.category,
            event.description or "",
        ]
        if value
    ).lower()

    country = event.country.strip().lower()

    # Regional GDP releases should not trigger broad GDP matching.
    is_regional_gdp = (
        "gdp" in title
        and any(
            phrase in title
            for phrase in ["by county", "by state", "regional"]
        )
    )

    if is_regional_gdp:
        matched_rules = []
    else:
        matched_rules = [
            rule
            for rule in EVENT_SECTOR_RULES
            if country in rule["countries"]
            and any(
                keyword in text
                for keyword in rule["keywords"]
            )
        ]

    relevant_sectors = {
        sector
        for rule in matched_rules
        for sector in rule["sectors"]
    }

    relevant_asset_classes = {
        asset_class
        for rule in matched_rules
        for asset_class in rule["asset_classes"]
    }

    matched_holdings = []
    unmatched_holdings = []

    for holding in holdings:
        symbol = str(holding.get("symbol", "")).strip().upper()

        if not symbol:
            continue

        exposure = get_holding_sector(symbol)

        holding_data = {
            "symbol": symbol,
            "company_name": holding.get("company_name") or symbol,
            "sector": exposure,
        }

        if exposure is None:
            unmatched_holdings.append(holding_data)
            continue

        if exposure in relevant_sectors:
            relevance = "potential_sector_exposure"
        elif exposure in relevant_asset_classes:
            if exposure in {"gold", "silver"}:
                relevance = "potential_commodity_exposure"
            else:
                relevance = "potential_broad_market_exposure"
        else:
            continue

        matched_holdings.append({
            **holding_data,
            "relevance": relevance,
        })

    if is_regional_gdp:
        explanation = (
            "This regional economic release is not matched to "
            "portfolio exposures because its direct relevance "
            "is unclear."
        )
    elif matched_holdings:
        explanation = " ".join(
            rule["reason"]
            for rule in matched_rules
        )
    elif not matched_rules:
        explanation = (
            "No specific event-exposure relationship is defined "
            "by the current matching rules."
        )
    else:
        explanation = (
            "No holdings with a mapped exposure matching this event "
            "were found. This does not rule out indirect market effects."
        )

    return {
        "event_title": event.title,
        "relevant_sectors": sorted(relevant_sectors),
        "relevant_asset_classes": sorted(relevant_asset_classes),
        "holdings": matched_holdings,
        "unmatched_holdings": unmatched_holdings,
        "explanation": explanation,
        "matching_method": "deterministic_rules",
    }
