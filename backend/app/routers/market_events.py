from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.market import MarketEconomicEventsResponse
from app.services.market_events_service import get_market_events

router = APIRouter(
    prefix="/market/events",
    tags=["Market"],
)


@router.get(
    "",
    response_model=MarketEconomicEventsResponse,
)
def read_market_events(
    db: Session = Depends(get_db),
) -> MarketEconomicEventsResponse:
    return get_market_events(db)
