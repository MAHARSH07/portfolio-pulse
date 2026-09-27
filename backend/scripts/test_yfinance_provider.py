from app.market_data.yfinance_market_data import (
    YFinanceMarketDataProvider,
)


def main() -> None:
    provider = YFinanceMarketDataProvider()

    prices = provider.get_prices(
        [
            "KPITTECH",
            "ZAGGLE",
            "NIFTYBEES",
            "GOLDIETF",
            "SILVERIETF",
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