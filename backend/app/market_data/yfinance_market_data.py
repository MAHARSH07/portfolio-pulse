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

        yahoo_symbols = [
            f"{symbol}.NS"
            for symbol in symbols
        ]

        try:
            tickers = yf.Tickers(" ".join(yahoo_symbols))
        except Exception:
            return {
                symbol: PriceSnapshot(
                    symbol=symbol,
                    price=None,
                    timestamp=timestamp,
                    source="yfinance",
                    status=PriceStatus.UNAVAILABLE,
                )
                for symbol in symbols
            }

        prices: dict[str, PriceSnapshot] = {}

        for symbol, yahoo_symbol in zip(
            symbols,
            yahoo_symbols,
        ):
            try:
                ticker = tickers.tickers[yahoo_symbol]
                price = ticker.fast_info.last_price
            except Exception:
                price = None

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
                price=Decimal(str(price)).quantize(Decimal("0.01")),
                timestamp=timestamp,
                source="yfinance",
                status=PriceStatus.DELAYED,
            )

        return prices