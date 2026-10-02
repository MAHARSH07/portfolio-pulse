from sqlalchemy.orm import Session
from langchain_core.tools import tool

from app.db.database import SessionLocal
from app.services.portfolio_service import get_holding_details


# Common aliases that may be used when referring to portfolio holdings.
SYMBOL_ALIASES = {
    "KPIT": "KPITTECH",
    "KPIT TECHNOLOGIES": "KPITTECH",
    "KPIT TECHNOLOGIES LIMITED": "KPITTECH",
}


@tool
def get_holding_tool(symbol: str) -> dict:
    """
    Get the user's current portfolio position for a specific stock or ETF.

    Accepts the exact trading symbol when possible, as well as common
    company-name or ticker aliases.
    """

    normalized_symbol = symbol.strip().upper()
    resolved_symbol = SYMBOL_ALIASES.get(
        normalized_symbol,
        normalized_symbol,
    )

    db: Session = SessionLocal()

    try:
        holding = get_holding_details(
            db=db,
            symbol=resolved_symbol,
        )

        if holding is None:
            return {
                "found": False,
                "requested_symbol": normalized_symbol,
                "resolved_symbol": resolved_symbol,
                "message": (
                    f"No holding found for {normalized_symbol} "
                    f"(looked up as {resolved_symbol})."
                ),
            }

        return {
            "found": True,
            "requested_symbol": normalized_symbol,
            "symbol": holding.symbol,
            "company_name": holding.company_name,
            "quantity": holding.quantity,
            "average_price": str(holding.average_price),
            "current_price": str(holding.current_price),
            "invested_value": str(holding.invested_value),
            "current_value": str(holding.current_value),
            "pnl": str(holding.pnl),
            "pnl_percentage": str(holding.pnl_percentage),
            "price_source": holding.price_source,
            "price_status": holding.price_status,
            "price_timestamp": (
                holding.price_timestamp.isoformat()
                if holding.price_timestamp
                else None
            ),
        }

    finally:
        db.close()