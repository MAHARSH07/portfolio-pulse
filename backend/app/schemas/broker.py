from decimal import Decimal

from pydantic import BaseModel, Field


class BrokerHolding(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    isin: str | None = None
    company_name: str | None = None
    quantity: Decimal = Field(gt=0)
    average_price: Decimal = Field(gt=0)


class BrokerTransaction(BaseModel):
    broker_trade_id: str
    symbol: str = Field(min_length=1, max_length=20)
    transaction_type: str
    quantity: Decimal = Field(gt=0)
    price: Decimal = Field(gt=0)