from sqlalchemy.orm import Session

from app.repositories.transaction_repository import get_transactions
from app.schemas.transaction import Transaction


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