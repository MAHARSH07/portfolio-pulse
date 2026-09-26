from fastapi import APIRouter, HTTPException

from app.brokers.groww.client import GrowwClient
from app.schemas.broker import BrokerHolding


router = APIRouter(
    prefix="/brokers/groww",
    tags=["Groww"],
)


@router.get(
    "/holdings",
    response_model=list[BrokerHolding],
)
def get_groww_holdings():
    try:
        client = GrowwClient()

        return client.get_holdings()

    except ValueError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch holdings from Groww.",
        ) from exc