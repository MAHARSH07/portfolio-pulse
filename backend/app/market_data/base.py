from abc import ABC, abstractmethod
from decimal import Decimal


class MarketDataProvider(ABC):

    @abstractmethod
    def get_prices(
        self,
        symbols: list[str],
    ) -> dict[str, Decimal]:
        pass