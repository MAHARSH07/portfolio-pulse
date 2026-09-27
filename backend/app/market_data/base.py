from abc import ABC, abstractmethod

from app.market_data.price import PriceSnapshot


class MarketDataProvider(ABC):
    @abstractmethod
    def get_prices(
        self,
        symbols: list[str],
    ) -> dict[str, PriceSnapshot]:
        pass