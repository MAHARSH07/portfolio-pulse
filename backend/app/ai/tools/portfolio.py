from sqlalchemy.orm import Session
from langchain_core.tools import tool

from app.db.database import SessionLocal
from app.services.portfolio_service import get_portfolio


@tool
def get_portfolio_tool() -> dict:
    """
    Get the user's current investment portfolio, including holdings,
    invested value, current value, and profit or loss.
    """

    db: Session = SessionLocal()

    try:
        portfolio = get_portfolio(db)

        return {
            "holdings": [
                {
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
                for holding in portfolio.holdings
            ],
            "total_invested": str(portfolio.total_invested),
            "total_current_value": str(portfolio.total_current_value),
            "total_pnl": str(portfolio.total_pnl),
            "total_pnl_percentage": str(portfolio.total_pnl_percentage),
        }

    finally:
        db.close()