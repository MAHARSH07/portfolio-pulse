from decimal import Decimal

from sqlalchemy import select

from app.db.database import Base, SessionLocal, engine
from app.models.holding import HoldingModel


INITIAL_HOLDINGS = [
    HoldingModel(
        symbol="KPIT",
        company_name="KPIT Technologies",
        quantity=10,
        average_price=Decimal("900.00"),
        current_price=Decimal("950.00"),
    ),
    HoldingModel(
        symbol="INFY",
        company_name="Infosys",
        quantity=5,
        average_price=Decimal("1500.00"),
        current_price=Decimal("1540.00"),
    ),
    HoldingModel(
        symbol="TCS",
        company_name="Tata Consultancy Services",
        quantity=3,
        average_price=Decimal("3500.00"),
        current_price=Decimal("3420.00"),
    ),
]


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        existing_holding = db.scalars(
            select(HoldingModel).limit(1)
        ).first()

        if existing_holding:
            print("Holdings already exist. Skipping seed.")
            return

        db.add_all(INITIAL_HOLDINGS)
        db.commit()

        print("Database initialized and holdings seeded.")

    finally:
        db.close()


if __name__ == "__main__":
    initialize_database()