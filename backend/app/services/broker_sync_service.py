from sqlalchemy import select
from sqlalchemy.orm import Session

from app.brokers.base import BrokerClient
from app.models.holding import HoldingModel

def sync_holdings(
    db: Session,
    broker_client: BrokerClient,
    broker_name: str,
) -> list[HoldingModel]:

    broker_holdings = broker_client.get_holdings()

    synchronized_holdings: list[HoldingModel] = []

    incoming_symbols = {
        holding.symbol
        for holding in broker_holdings
    }

    existing_holdings = list(
        db.scalars(
            select(HoldingModel).where(
                HoldingModel.broker == broker_name
            )
        ).all()
    )

    existing_by_symbol = {
        holding.symbol: holding
        for holding in existing_holdings
    }

    for broker_holding in broker_holdings:
        existing_holding = existing_by_symbol.get(
            broker_holding.symbol
        )

        if existing_holding:
            existing_holding.company_name = (
                broker_holding.company_name
            )
            existing_holding.quantity = (
                broker_holding.quantity
            )
            existing_holding.average_price = (
                broker_holding.average_price
            )

            synchronized_holdings.append(
                existing_holding
            )

        else:
            new_holding = HoldingModel(
                symbol=broker_holding.symbol,
                company_name=broker_holding.company_name,
                quantity=broker_holding.quantity,
                average_price=broker_holding.average_price,
                broker=broker_name,
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