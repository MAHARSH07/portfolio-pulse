from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.holding import HoldingModel
from app.models.instrument import InstrumentModel

def main() -> None:
    db = SessionLocal()

    try:
        holding = db.scalars(
            select(HoldingModel)
            .where(HoldingModel.symbol == "KPITTECH")
        ).first()

        if holding is None:
            raise RuntimeError("KPITTECH holding was not found.")

        print("Holding:")
        print(f"Symbol: {holding.symbol}")
        print(f"Instrument ID: {holding.instrument_id}")

        print("\nInstrument:")
        print(f"Symbol: {holding.instrument.trading_symbol}")
        print(f"Name: {holding.instrument.name}")
        print(f"ISIN: {holding.instrument.isin}")
        print(f"Exchange: {holding.instrument.exchange}")

    finally:
        db.close()


if __name__ == "__main__":
    main()