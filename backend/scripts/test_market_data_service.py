from app.market_data.groww_market_data import (
    GrowwMarketDataProvider,
)
from app.market_data.yfinance_market_data import (
    YFinanceMarketDataProvider,
)
from app.services.market_data_service import MarketDataService


def main() -> None:
    service = MarketDataService(
        primary_provider=GrowwMarketDataProvider(),
        fallback_provider=YFinanceMarketDataProvider(),
    )

    prices = service.get_prices(
        [
            "KPITTECH",
            "ZAGGLE",
            "NIFTYBEES",
        ]
    )

    for symbol, snapshot in prices.items():
        print(symbol)
        print(f"  Price:   {snapshot.price}")
        print(f"  Source:  {snapshot.source}")
        print(f"  Status:  {snapshot.status}")
        print(f"  Time:    {snapshot.timestamp}")
        print()


if __name__ == "__main__":
    main()