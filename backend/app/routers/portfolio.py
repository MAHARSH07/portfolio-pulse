from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.portfolio import Portfolio
from app.services.portfolio_service import get_portfolio


router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"],
)


@router.get("", response_model=Portfolio)
def read_portfolio(
    db: Session = Depends(get_db),
) -> Portfolio:
    return get_portfolio(db)