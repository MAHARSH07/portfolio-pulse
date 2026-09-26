from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.transaction import TransactionModel


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