
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


def get_holding_explanation(
    rule_ids: set[str],
    exposure: str,
) -> str:
    """Explain the potential connection for an individual holding."""

    if exposure == "gold":
        return (
            "Gold prices can respond to interest-rate expectations, "
            "currency movements, and investor demand for safe-haven "
            "assets. The actual effect depends on market conditions."
        )

    if exposure == "silver":
        return (
            "Silver can respond to precious-metal demand, currency "
            "movements, and industrial demand. The effect depends "
            "on the event and broader market conditions."
        )

    if exposure == "banking":
        if "rbi_policy" in rule_ids:
            return (
                "RBI policy decisions can influence Indian interest "
                "rates, bank funding costs, lending conditions, and "
                "credit demand. The net effect on banking stocks "
                "is not necessarily positive or negative."
            )

        return (
            "This banking exposure may be affected indirectly by "
            "interest-rate expectations, liquidity, and investor "
            "flows. The effect depends on the event and market context."
        )

    if exposure == "financial_services":
        return (
            "Financial-services businesses may be affected by "
            "interest rates, liquidity, borrowing conditions, and "
            "investor activity. The impact varies by business model."
        )

    if exposure == "technology":
        return (
            "Technology-sector sentiment can respond to global "
            "growth expectations, currency movements, and changes "
            "in investor risk appetite. Company-specific factors "
            "can lead to different outcomes."
        )

    if exposure == "exporters":
        return (
            "Export-oriented businesses may be affected by overseas "
            "demand, trade conditions, and currency movements. The "
            "impact depends on their markets and business mix."
        )

    if exposure == "manufacturing":
        return (
            "Manufacturing businesses may be affected by demand "
            "conditions, input costs, trade activity, and economic "
            "growth expectations."
        )

    if exposure == "industrials":
        return (
            "Industrial businesses can be sensitive to economic "
            "activity, trade flows, and investment demand. The "
            "actual impact varies across companies."
        )

    if exposure == "energy":
        return (
            "Energy-sector performance may respond to economic "
            "activity, energy demand, and commodity-market conditions."
        )

    if exposure == "consumer":
        return (
            "Consumer-facing businesses may be affected by household "
            "income, spending patterns, and inflation."
        )

    if exposure == "retail":
        return (
            "Retail businesses may be affected by consumer spending, "
            "purchasing power, and changes in household demand."
        )

    if exposure in {"broad_market_equity", "midcap_equity"}:
        market_type = (
            "Mid-cap equities"
            if exposure == "midcap_equity"
            else "Broad-market equities"
        )
        return (
            f"{market_type} may respond to changes in economic-growth "
            "expectations, interest rates, and investor sentiment. "
            "The effect depends on the event and market conditions."
        )

    return (
        "This holding matches a broad exposure category for the event. "
        "Its specific sensitivity has not been established."
    )


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
    matched_rule_ids = {
        rule["id"] for rule in matched_rules
    }

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
            "holding_explanation": get_holding_explanation(
                matched_rule_ids,
                exposure,
            ),
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
