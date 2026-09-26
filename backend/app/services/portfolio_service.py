from sqlalchemy.orm import Session

from app.repositories.portfolio_repository import get_holdings
from app.schemas.portfolio import Holding, Portfolio


def get_portfolio(db: Session) -> Portfolio:
    holding_models = get_holdings(db)

    holdings = [
        Holding.model_validate(holding_model)
        for holding_model in holding_models
    ]

    total_invested = sum(
        holding.invested_value
        for holding in holdings
    )

    total_current_value = sum(
        holding.current_value
        for holding in holdings
    )

    total_pnl = total_current_value - total_invested

    total_pnl_percentage = (
        (total_pnl / total_invested) * 100
        if total_invested
        else 0.0
    )

    return Portfolio(
        holdings=holdings,
        total_invested=total_invested,
        total_current_value=total_current_value,
        total_pnl=total_pnl,
        total_pnl_percentage=total_pnl_percentage,
    )