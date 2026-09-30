from sqlalchemy.orm import Session
from langchain_core.tools import tool

from app.db.database import SessionLocal
from app.services.portfolio_service import get_holding_details


@tool
def get_holding_tool(symbol: str) -> dict:
    """
    Get the user's current portfolio position for a specific stock or ETF symbol.
    Use the exact trading symbol when possible.
    """

    db: Session = SessionLocal()

    try:
        holding = get_holding_details(
            db=db,
            symbol=symbol.upper(),
        )

        if holding is None:
            return {
                "found": False,
                "symbol": symbol.upper(),
                "message": f"No holding found for {symbol.upper()}.",
            }

        return {
            "found": True,
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