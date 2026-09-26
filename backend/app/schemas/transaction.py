from datetime import datetime

from pydantic import BaseModel, ConfigDict, computed_field


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