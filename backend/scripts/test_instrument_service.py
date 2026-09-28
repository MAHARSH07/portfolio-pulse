from app.brokers.groww.client import GrowwClient
from app.db.database import SessionLocal
from app.services.instrument_service import InstrumentService


def main() -> None:
    db = SessionLocal()

    try:
        broker_client = GrowwClient()
        service = InstrumentService(broker_client)

        instrument = service.get_or_create_instrument(
            db=db,
            trading_symbol="KPITTECH",
        )

        db.commit()

        print("Instrument stored:")
        print(f"ID: {instrument.id}")
        print(f"Symbol: {instrument.trading_symbol}")
        print(f"Name: {instrument.name}")
        print(f"ISIN: {instrument.isin}")
        print(f"Exchange: {instrument.exchange}")
        print(f"Groww symbol: {instrument.groww_symbol}")
    finally:
        db.close()


if __name__ == "__main__":
    main()