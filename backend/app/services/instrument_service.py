from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.brokers.groww.client import GrowwClient
from app.models.instrument import InstrumentModel
from app.repositories.instrument_repository import (
    create_instrument,
    get_instrument_by_trading_symbol,
)
from app.schemas.instrument import BrokerInstrument


class InstrumentService:
    def __init__(self, broker_client: GrowwClient):
        self.broker_client = broker_client

    def get_or_create_instrument(
        self,
        db: Session,
        trading_symbol: str,
    ) -> InstrumentModel:
        existing_instrument = get_instrument_by_trading_symbol(
            db=db,
            trading_symbol=trading_symbol,
        )

        if existing_instrument:
            return existing_instrument

        broker_instrument = self.broker_client.get_instrument(
            trading_symbol=trading_symbol,
        )

        now = datetime.now(timezone.utc)

        instrument = InstrumentModel(
            isin=broker_instrument.isin,
            trading_symbol=broker_instrument.trading_symbol,
            groww_symbol=broker_instrument.groww_symbol,
            name=broker_instrument.name,
            exchange=broker_instrument.exchange,
            exchange_token=broker_instrument.exchange_token,
            instrument_type=broker_instrument.instrument_type,
            segment=broker_instrument.segment,
            series=broker_instrument.series,
            lot_size=broker_instrument.lot_size,
            tick_size=broker_instrument.tick_size,
            created_at=now,
            updated_at=now,
        )

        return create_instrument(
            db=db,
            instrument=instrument,
        )