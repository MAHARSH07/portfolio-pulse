from datetime import datetime, timezone
from decimal import Decimal

from growwapi.groww.exceptions import GrowwAPIException

from app.brokers.groww.client import GrowwClient
from app.market_data.base import MarketDataProvider
from app.market_data.price import PriceSnapshot, PriceStatus


class GrowwMarketDataProvider(MarketDataProvider):
    def __init__(self, client: GrowwClient | None = None):
        self.client = client or GrowwClient()

    def get_prices(
        self,
        symbols: list[str],
    ) -> dict[str, PriceSnapshot]:
        if not symbols:
            return {}

        exchange_symbols = tuple(
            f"NSE_{symbol}" for symbol in symbols
        )

        timestamp = datetime.now(timezone.utc)

        try:
            response = self.client.client.get_ltp(
                segment=self.client.client.SEGMENT_CASH,
                exchange_trading_symbols=exchange_symbols,
            )
        except GrowwAPIException:
            return {
                symbol: PriceSnapshot(
                    symbol=symbol,
                    price=None,
                    timestamp=timestamp,
                    source="groww",
                    status=PriceStatus.UNAVAILABLE,
                )
                for symbol in symbols
            }

        prices: dict[str, PriceSnapshot] = {}

        for symbol in symbols:
            price = response.get(f"NSE_{symbol}")

            if price is None:
                prices[symbol] = PriceSnapshot(
                    symbol=symbol,
                    price=None,
                    timestamp=timestamp,
                    source="groww",
                    status=PriceStatus.UNAVAILABLE,
                )
                continue

            prices[symbol] = PriceSnapshot(
                symbol=symbol,
                price=Decimal(str(price)),
                timestamp=timestamp,
                source="groww",
                status=PriceStatus.REAL_TIME,
            )

        return prices