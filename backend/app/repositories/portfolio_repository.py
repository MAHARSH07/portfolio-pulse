from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.holding import HoldingModel


def get_holdings(db: Session) -> list[HoldingModel]:
    statement = select(HoldingModel).order_by(HoldingModel.symbol)

    return list(db.scalars(statement).all())

def get_holding(db: Session, symbol: str) -> HoldingModel | None:
    statement = select(HoldingModel).where(
        HoldingModel.symbol == symbol
    )

    return db.scalars(statement).first()