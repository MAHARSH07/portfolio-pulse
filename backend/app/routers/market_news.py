from fastapi import APIRouter

from app.schemas.market import MarketNewsResponse
from app.services.market_news_service import get_market_news


router = APIRouter(
    prefix="/market/news",
    tags=["Market"],
)


@router.get("", response_model=MarketNewsResponse)
def read_market_news() -> MarketNewsResponse:
    return get_market_news()