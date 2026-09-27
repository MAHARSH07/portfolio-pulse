import yfinance as yf


def main() -> None:
    symbols = [
        "KPITTECH.NS",
        "ZAGGLE.NS",
        "NIFTYBEES.NS",
        "GOLDIETF.NS",
        "SILVERIETF.NS",
    ]

    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        info = ticker.fast_info

        print(symbol)
        print(f"  Price: {info.last_price}")
        print(f"  Previous close: {info.previous_close}")
        print()


if __name__ == "__main__":
    main()