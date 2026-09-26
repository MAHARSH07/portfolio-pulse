from sqlalchemy.orm import Session

from app.repositories.transaction_repository import (
    create_transaction,
    get_transactions,
)
from app.schemas.transaction import Transaction, TransactionCreate


def get_transaction_history(
    db: Session,
    symbol: str | None = None,
) -> list[Transaction]:
    transaction_models = get_transactions(
        db,
        symbol,
    )

    return [
        Transaction.model_validate(transaction_model)
        for transaction_model in transaction_models
    ]


def create_transaction_record(
    db: Session,
    transaction_data: TransactionCreate,
) -> Transaction:
    transaction_model = create_transaction(
        db,
        transaction_data,
    )

    return Transaction.model_validate(transaction_model)