from decimal import Decimal

from pydantic import BaseModel, ConfigDict, computed_field


class Holding(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: str
    company_name: str | None = None
    quantity: int
    average_price: Decimal
    current_price: Decimal

    @computed_field
    @property
    def invested_value(self) -> Decimal:
        return self.quantity * self.average_price

    @computed_field
    @property
    def current_value(self) -> Decimal:
        return self.quantity * self.current_price

    @computed_field
    @property
    def pnl(self) -> Decimal:
        return self.current_value - self.invested_value

    @computed_field
    @property
    def pnl_percentage(self) -> Decimal:
        if self.invested_value == 0:
            return Decimal("0")

        return ((self.pnl / self.invested_value) * Decimal("100")).quantize(Decimal("0.01"))


class Portfolio(BaseModel):
    holdings: list[Holding]
    total_invested: Decimal
    total_current_value: Decimal
    total_pnl: Decimal
    total_pnl_percentage: Decimal