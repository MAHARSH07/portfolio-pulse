from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel


class PriceStatus(StrEnum):
    REAL_TIME = "REAL_TIME"
    DELAYED = "DELAYED"
    EOD = "EOD"
    UNAVAILABLE = "UNAVAILABLE"


class PriceSnapshot(BaseModel):
    symbol: str
    price: Decimal | None
    timestamp: datetime | None
    source: str
    status: PriceStatus