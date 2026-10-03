from datetime import datetime, timezone
from decimal import Decimal

import yfinance as yf

from app.market_data.price import PriceStatus
from app.schemas.market import MarketInstrument


MARKET_INSTRUMENTS = [
    {
        "name": "NIFTY 50",
        "symbol": "^NSEI",
    },
    {
        "name": "Sensex",
        "symbol": "^BSESN",
    },
    {
        "name": "Nifty Bank",
        "symbol": "^NSEBANK",
    },
    {
        "name": "Gold",
        "symbol": "GC=F",
    },
    {
        "name": "Silver",
        "symbol": "SI=F",
    },
    {
        "name": "S&P 500",
        "symbol": "^GSPC",
    },
    {
        "name": "NASDAQ",
        "symbol": "^IXIC",
    },
    {
        "name": "Dow Jones",
        "symbol": "^DJI",
    },
]


class MarketOverviewProvider:

    def get_market_overview(self) -> list[MarketInstrument]:
        symbols = [
            instrument["symbol"]
            for instrument in MARKET_INSTRUMENTS
        ]

        timestamp = datetime.now(timezone.utc)

        tickers = yf.Tickers(" ".join(symbols))

        instruments = []

        for instrument in MARKET_INSTRUMENTS:
            symbol = instrument["symbol"]
            ticker = tickers.tickers[symbol]

            try:
                current_value = ticker.fast_info.last_price
                previous_close = ticker.fast_info.previous_close
            except Exception:
                continue

            if current_value is None or previous_close is None:
                continue

            current_value = Decimal(str(current_value))
            previous_close = Decimal(str(previous_close))

            change = current_value - previous_close

            change_percentage = (
                (change / previous_close) * Decimal("100")
                if previous_close != 0
                else Decimal("0")
            )

            instruments.append(
                MarketInstrument(
                    name=instrument["name"],
                    symbol=symbol,
                    value=current_value.quantize(Decimal("0.01")),
                    previous_close=previous_close.quantize(
                        Decimal("0.01")
                    ),
                    change=change.quantize(Decimal("0.01")),
                    change_percentage=change_percentage.quantize(
                        Decimal("0.01")
                    ),
                    source="yfinance",
                    status=PriceStatus.DELAYED,
                    timestamp=timestamp,
                )
            )

        return instruments