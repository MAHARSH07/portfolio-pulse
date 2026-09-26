from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select

from app.db.database import Base, SessionLocal, engine
from app.models.holding import HoldingModel
from app.models.transaction import TransactionModel


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


INITIAL_TRANSACTIONS = [
    TransactionModel(
        symbol="KPIT",
        transaction_type="BUY",
        quantity=5,
        price=Decimal("850.00"),
        transaction_date=datetime(
            2026,
            1,
            15,
            tzinfo=timezone.utc,
        ),
    ),
    TransactionModel(
        symbol="KPIT",
        transaction_type="BUY",
        quantity=5,
        price=Decimal("950.00"),
        transaction_date=datetime(
            2026,
            2,
            20,
            tzinfo=timezone.utc,
        ),
    ),
    TransactionModel(
        symbol="INFY",
        transaction_type="BUY",
        quantity=5,
        price=Decimal("1500.00"),
        transaction_date=datetime(
            2026,
            1,
            25,
            tzinfo=timezone.utc,
        ),
    ),
    TransactionModel(
        symbol="TCS",
        transaction_type="BUY",
        quantity=3,
        price=Decimal("3500.00"),
        transaction_date=datetime(
            2026,
            2,
            10,
            tzinfo=timezone.utc,
        ),
    ),
]


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        existing_holding = db.scalars(
            select(HoldingModel).limit(1)
        ).first()

        if not existing_holding:
            db.add_all(INITIAL_HOLDINGS)

        existing_transaction = db.scalars(
            select(TransactionModel).limit(1)
        ).first()

        if not existing_transaction:
            db.add_all(INITIAL_TRANSACTIONS)

        db.commit()

        print("Database initialization completed.")

    finally:
        db.close()


if __name__ == "__main__":
    initialize_database()