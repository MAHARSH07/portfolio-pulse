from app.market_data.twelve_data import TwelveDataProvider


def main():
    provider = TwelveDataProvider()

    prices = provider.get_prices(
        ["INFY"]
    )

    print("Price request succeeded.")
    print("Prices:", prices)


if __name__ == "__main__":
    main()