from decimal import Decimal

from pydantic import BaseModel, Field


class BrokerHolding(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    company_name: str = Field(min_length=1, max_length=200)
    quantity: int = Field(gt=0)
    average_price: Decimal = Field(gt=0)


class BrokerTransaction(BaseModel):
    broker_trade_id: str
    symbol: str = Field(min_length=1, max_length=20)
    transaction_type: str
    quantity: int = Field(gt=0)
    price: Decimal = Field(gt=0)