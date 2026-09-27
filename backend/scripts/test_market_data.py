from app.market_data.groww_market_data import GrowwMarketDataProvider


def main() -> None:
    provider = GrowwMarketDataProvider()

    prices = provider.get_prices(
        [
            "KPITTECH",
            "ZAGGLE",
            "NIFTYBEES",
        ]
    )

    for symbol, snapshot in prices.items():
        print(symbol)
        print(f"  Price: {snapshot.price}")
        print(f"  Source: {snapshot.source}")
        print(f"  Status: {snapshot.status}")
        print(f"  Time:   {snapshot.timestamp}")
        print()


if __name__ == "__main__":
    main()