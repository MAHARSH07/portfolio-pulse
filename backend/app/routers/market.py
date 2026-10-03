from fastapi import APIRouter

from app.schemas.market import MarketOverview
from app.services.market_service import get_market_overview


router = APIRouter(
    prefix="/market",
    tags=["Market"],
)


@router.get("", response_model=MarketOverview)
def read_market_overview() -> MarketOverview:
    return get_market_overview()