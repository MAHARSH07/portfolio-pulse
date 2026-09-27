from decimal import Decimal

from pydantic import BaseModel


class BrokerInstrument(BaseModel):
    exchange: str
    exchange_token: str
    trading_symbol: str
    groww_symbol: str
    name: str | None = None
    instrument_type: str
    segment: str
    series: str | None = None
    isin: str | None = None
    lot_size: Decimal | None = None
    tick_size: Decimal | None = None