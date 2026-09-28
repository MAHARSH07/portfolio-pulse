from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.instrument import InstrumentModel


def get_instrument_by_trading_symbol(
    db: Session,
    trading_symbol: str,
) -> InstrumentModel | None:
    statement = select(InstrumentModel).where(
        InstrumentModel.trading_symbol == trading_symbol
    )

    return db.scalars(statement).first()


def create_instrument(
    db: Session,
    instrument: InstrumentModel,
) -> InstrumentModel:
    db.add(instrument)
    db.flush()
    return instrument