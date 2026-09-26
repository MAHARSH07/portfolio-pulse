from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.transaction import TransactionModel
from app.schemas.transaction import TransactionCreate


def get_transactions(
    db: Session,
    symbol: str | None = None,
) -> list[TransactionModel]:
    statement = select(TransactionModel)

    if symbol:
        statement = statement.where(
            TransactionModel.symbol == symbol.upper()
        )

    statement = statement.order_by(
        TransactionModel.transaction_date.desc()
    )

    return list(db.scalars(statement).all())


def create_transaction(
    db: Session,
    transaction_data: TransactionCreate,
) -> TransactionModel:
    transaction = TransactionModel(
        symbol=transaction_data.symbol,
        transaction_type=transaction_data.transaction_type,
        quantity=transaction_data.quantity,
        price=transaction_data.price,
        transaction_date=datetime.now(timezone.utc),
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction