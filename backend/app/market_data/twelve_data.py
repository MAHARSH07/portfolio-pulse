from decimal import Decimal

import httpx

from app.core.config import settings
from app.market_data.base import MarketDataProvider


class TwelveDataProvider(MarketDataProvider):

    BASE_URL = "https://api.twelvedata.com"

    def __init__(self, api_key: str | None = None):
        key = api_key or settings.twelve_data_api_key

        if not key:
            raise ValueError(
                "Twelve Data API key is not configured."
            )

        self.api_key = key

    def get_prices(
        self,
        symbols: list[str],
    ) -> dict[str, Decimal]:

        if not symbols:
            return {}

        provider_symbols = [
            f"{symbol}:NSE"
            for symbol in symbols
        ]

        params = {
            "symbol": ",".join(provider_symbols),
            "apikey": self.api_key,
        }

        with httpx.Client(timeout=5) as client:
            response = client.get(
                f"{self.BASE_URL}/price",
                params=params,
            )

        response.raise_for_status()

        data = response.json()

        if not isinstance(data, dict):
            raise RuntimeError(
                "Unexpected response from Twelve Data."
            )

        prices: dict[str, Decimal] = {}

        if "price" in data:
            symbol = symbols[0]

            prices[symbol] = Decimal(
                str(data["price"])
            )

            return prices

        for provider_symbol, result in data.items():
            if not isinstance(result, dict):
                continue

            price = result.get("price")

            if price is None:
                continue

            symbol = provider_symbol.split(":")[0]

            prices[symbol] = Decimal(str(price))

        return prices