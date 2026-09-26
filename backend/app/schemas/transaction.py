from datetime import datetime

from pydantic import BaseModel, ConfigDict, computed_field, Field, field_validator


class TransactionCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    transaction_type: str
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("transaction_type")
    @classmethod
    def validate_transaction_type(cls, value: str) -> str:
        value = value.strip().upper()

        if value not in {"BUY", "SELL"}:
            raise ValueError("Transaction type must be BUY or SELL")

        return value


class Transaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    symbol: str
    transaction_type: str
    quantity: int
    price: float
    transaction_date: datetime

    @computed_field
    @property
    def total_amount(self) -> float:
        return self.quantity * self.price