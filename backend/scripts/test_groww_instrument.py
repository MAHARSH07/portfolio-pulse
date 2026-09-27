from app.brokers.groww.client import GrowwClient


def main() -> None:
    client = GrowwClient()

    instrument = client.get_instrument("KPITTECH")

    print("Instrument details:")
    print(instrument)


if __name__ == "__main__":
    main()