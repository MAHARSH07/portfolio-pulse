from decimal import Decimal

from app.brokers.base import BrokerClient
from app.schemas.broker import BrokerHolding, BrokerTransaction


class MockBrokerClient(BrokerClient):

    def get_holdings(self) -> list[BrokerHolding]:
        return [
            BrokerHolding(
                symbol="KPIT",
                company_name="KPIT Technologies",
                quantity=10,
                average_price=Decimal("900.00"),
            ),
            BrokerHolding(
                symbol="INFY",
                company_name="Infosys",
                quantity=5,
                average_price=Decimal("1500.00"),
            ),
            BrokerHolding(
                symbol="TCS",
                company_name="Tata Consultancy Services",
                quantity=3,
                average_price=Decimal("3500.00"),
            ),
        ]

    def get_transactions(self) -> list[BrokerTransaction]:
        return [
            BrokerTransaction(
                broker_trade_id="MOCK-KPIT-001",
                symbol="KPIT",
                transaction_type="BUY",
                quantity=5,
                price=Decimal("850.00"),
            ),
            BrokerTransaction(
                broker_trade_id="MOCK-KPIT-002",
                symbol="KPIT",
                transaction_type="BUY",
                quantity=5,
                price=Decimal("950.00"),
            ),
            BrokerTransaction(
                broker_trade_id="MOCK-INFY-001",
                symbol="INFY",
                transaction_type="BUY",
                quantity=5,
                price=Decimal("1500.00"),
            ),
            BrokerTransaction(
                broker_trade_id="MOCK-TCS-001",
                symbol="TCS",
                transaction_type="BUY",
                quantity=3,
                price=Decimal("3500.00"),
            ),
        ]