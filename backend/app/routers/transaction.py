from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.transaction import Transaction, TransactionCreate
from app.services.transaction_service import (
    create_transaction_record,
    get_transaction_history,
)


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.get("", response_model=list[Transaction])
def read_transactions(
    symbol: str | None = Query(
        default=None,
        min_length=1,
        max_length=20,
    ),
    db: Session = Depends(get_db),
) -> list[Transaction]:
    return get_transaction_history(
        db,
        symbol,
    )


@router.post(
    "",
    response_model=Transaction,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
) -> Transaction:
    return create_transaction_record(
        db,
        transaction_data,
    )