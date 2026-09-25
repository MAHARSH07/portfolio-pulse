from fastapi import APIRouter

from app.schemas.portfolio import Portfolio
from app.services.portfolio_service import get_portfolio


router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"],
)


@router.get("", response_model=Portfolio)
def read_portfolio() -> Portfolio:
    return get_portfolio()