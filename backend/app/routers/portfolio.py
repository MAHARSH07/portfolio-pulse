from fastapi import APIRouter

from app.data.portfolio import MOCK_HOLDINGS
from app.schemas.portfolio import Portfolio


router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"],
)


@router.get("", response_model=Portfolio)
def get_portfolio():
    total_invested = sum(
        holding.invested_value
        for holding in MOCK_HOLDINGS
    )

    total_current_value = sum(
        holding.current_value
        for holding in MOCK_HOLDINGS
    )

    total_pnl = total_current_value - total_invested

    total_pnl_percentage = (
        (total_pnl / total_invested) * 100
        if total_invested
        else 0.0
    )

    return Portfolio(
        holdings=MOCK_HOLDINGS,
        total_invested=total_invested,
        total_current_value=total_current_value,
        total_pnl=total_pnl,
        total_pnl_percentage=total_pnl_percentage,
    )