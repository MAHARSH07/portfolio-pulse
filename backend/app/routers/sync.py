from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.brokers.mock import MockBrokerClient
from app.db.database import get_db
from app.services.broker_sync_service import sync_holdings


router = APIRouter(
    prefix="/sync",
    tags=["Synchronization"],
)


@router.post("/portfolio")
def synchronize_portfolio(
    db: Session = Depends(get_db),
):
    broker_client = MockBrokerClient()

    holdings = sync_holdings(
        db=db,
        broker_client=broker_client,
        broker_name="mock",
    )

    return {
        "message": "Portfolio synchronized successfully",
        "holdings_synced": len(holdings),
    }