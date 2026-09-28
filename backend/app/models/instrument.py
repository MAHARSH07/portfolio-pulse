from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.holding import HoldingModel
from app.db.database import Base


class InstrumentModel(Base):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    isin: Mapped[str | None] = mapped_column(
        String(20),
        unique=True,
        nullable=True,
    )

    trading_symbol: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    groww_symbol: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    exchange: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    exchange_token: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    instrument_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    segment: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    series: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    lot_size: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 6),
        nullable=True,
    )

    tick_size: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 6),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    holdings: Mapped[list["HoldingModel"]] = relationship(
        "HoldingModel",
        back_populates="instrument",
    )
