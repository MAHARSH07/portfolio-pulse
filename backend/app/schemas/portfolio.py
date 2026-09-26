from pydantic import BaseModel, ConfigDict, computed_field


class Holding(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: str
    company_name: str | None = None
    quantity: int
    average_price: float
    current_price: float

    @computed_field
    @property
    def invested_value(self) -> float:
        return self.quantity * self.average_price

    @computed_field
    @property
    def current_value(self) -> float:
        return self.quantity * self.current_price

    @computed_field
    @property
    def pnl(self) -> float:
        return self.current_value - self.invested_value

    @computed_field
    @property
    def pnl_percentage(self) -> float:
        if self.invested_value == 0:
            return 0.0

        return (self.pnl / self.invested_value) * 100


class Portfolio(BaseModel):
    holdings: list[Holding]
    total_invested: float
    total_current_value: float
    total_pnl: float
    total_pnl_percentage: float