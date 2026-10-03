from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.market_data.price import PriceStatus


class MarketInstrument(BaseModel):
    name: str
    symbol: str
    value: Decimal
    previous_close: Decimal
    change: Decimal
    change_percentage: Decimal
    source: str
    status: PriceStatus
    timestamp: datetime


class MarketOverview(BaseModel):
    instruments: list[MarketInstrument]