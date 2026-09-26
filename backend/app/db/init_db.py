from app.db.database import Base, engine

# Import models so SQLAlchemy registers their tables.
from app.models.holding import HoldingModel
from app.models.transaction import TransactionModel


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)

    print("Database tables initialized.")


if __name__ == "__main__":
    initialize_database()