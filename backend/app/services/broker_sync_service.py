from sqlalchemy import select
from sqlalchemy.orm import Session

from app.brokers.base import BrokerClient
from app.models.holding import HoldingModel
from app.services.instrument_service import InstrumentService


def sync_holdings(
    db: Session,
    broker_client: BrokerClient,
    broker_name: str,
) -> list[HoldingModel]:

    broker_holdings = broker_client.get_holdings()
    instrument_service = InstrumentService(broker_client)

    synchronized_holdings: list[HoldingModel] = []

    incoming_symbols = {holding.symbol for holding in broker_holdings}

    existing_holdings = list(
        db.scalars(select(HoldingModel).where(HoldingModel.broker == broker_name)).all()
    )

    existing_by_symbol = {holding.symbol: holding for holding in existing_holdings}

    for broker_holding in broker_holdings:
        instrument = instrument_service.get_or_create_instrument(
            db=db,
            trading_symbol=broker_holding.symbol,
        )
        existing_holding = existing_by_symbol.get(broker_holding.symbol)

        if existing_holding:
            existing_holding.quantity = broker_holding.quantity
            existing_holding.average_price = broker_holding.average_price
            existing_holding.instrument_id = instrument.id

            synchronized_holdings.append(existing_holding)

        else:
            new_holding = HoldingModel(
                symbol=broker_holding.symbol,
                quantity=broker_holding.quantity,
                average_price=broker_holding.average_price,
                broker=broker_name,
                instrument_id=instrument.id,
            )

            db.add(new_holding)
            synchronized_holdings.append(new_holding)

    for existing_holding in existing_holdings:
        if existing_holding.symbol not in incoming_symbols:
            db.delete(existing_holding)

    db.commit()

    for holding in synchronized_holdings:
        db.refresh(holding)

    return synchronized_holdings
