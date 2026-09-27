from app.market_data.base import MarketDataProvider
from app.market_data.price import PriceSnapshot, PriceStatus


class MarketDataService:
    def __init__(
        self,
        primary_provider: MarketDataProvider,
        fallback_provider: MarketDataProvider,
    ):
        self.primary_provider = primary_provider
        self.fallback_provider = fallback_provider

    def get_prices(
        self,
        symbols: list[str],
    ) -> dict[str, PriceSnapshot]:
        if not symbols:
            return {}

        primary_prices = self.primary_provider.get_prices(symbols)

        unavailable_symbols = [
            symbol
            for symbol in symbols
            if (
                symbol not in primary_prices
                or primary_prices[symbol].status
                == PriceStatus.UNAVAILABLE
            )
        ]

        if not unavailable_symbols:
            return primary_prices

        fallback_prices = self.fallback_provider.get_prices(
            unavailable_symbols
        )

        prices = dict(primary_prices)

        for symbol in unavailable_symbols:
            fallback_snapshot = fallback_prices.get(symbol)

            if (
                fallback_snapshot is not None
                and fallback_snapshot.status
                != PriceStatus.UNAVAILABLE
            ):
                prices[symbol] = fallback_snapshot

        return prices