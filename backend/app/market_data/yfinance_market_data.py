from datetime import datetime, timezone
from decimal import Decimal

import yfinance as yf

from app.market_data.base import MarketDataProvider
from app.market_data.price import PriceSnapshot, PriceStatus


class YFinanceMarketDataProvider(MarketDataProvider):
    def get_prices(
        self,
        symbols: list[str],
    ) -> dict[str, PriceSnapshot]:
        if not symbols:
            return {}

        timestamp = datetime.now(timezone.utc)
        prices: dict[str, PriceSnapshot] = {}

        for symbol in symbols:
            yahoo_symbol = f"{symbol}.NS"

            try:
                ticker = yf.Ticker(yahoo_symbol)
                price = ticker.fast_info.last_price
            except Exception:
                prices[symbol] = PriceSnapshot(
                    symbol=symbol,
                    price=None,
                    timestamp=timestamp,
                    source="yfinance",
                    status=PriceStatus.UNAVAILABLE,
                )
                continue

            if price is None:
                prices[symbol] = PriceSnapshot(
                    symbol=symbol,
                    price=None,
                    timestamp=timestamp,
                    source="yfinance",
                    status=PriceStatus.UNAVAILABLE,
                )
                continue

            prices[symbol] = PriceSnapshot(
                symbol=symbol,
                price=Decimal(str(price)),
                timestamp=timestamp,
                source="yfinance",
                status=PriceStatus.DELAYED,
            )

        return prices