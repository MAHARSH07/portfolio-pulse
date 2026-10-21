# Maps known portfolio symbols to their exposure categories.
#
# These mappings support event relevance only. They do not predict
# price movements or constitute investment recommendations.

SECTOR_MAPPINGS: dict[str, str] = {
    # Individual stocks
    "KPITTECH": "technology",
    "CONTROLPR": "manufacturing",
    "GUJENERGY": "energy",
    "JWL": "industrials",
    "ZAGGLE": "financial_services",

    # Banking ETFs
    "BANKBEES": "banking",
    "PSUBNKBEES": "banking",

    # Broad-market and diversified equity ETFs
    "NIFTYBEES": "broad_market_equity",
    "MIDCAPETF": "midcap_equity",

    # Commodity ETFs
    "GOLDIETF": "gold",
    "SILVERIETF": "silver",
}


def get_holding_sector(symbol: str) -> str | None:
    """
    Return the mapped exposure category for a portfolio symbol.

    Returns None for symbols that have not been mapped.
    """
    normalized_symbol = symbol.strip().upper()
    return SECTOR_MAPPINGS.get(normalized_symbol)