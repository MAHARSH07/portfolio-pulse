from abc import ABC, abstractmethod

from app.schemas.broker import BrokerHolding, BrokerTransaction


class BrokerClient(ABC):

    @abstractmethod
    def get_holdings(self) -> list[BrokerHolding]:
        pass

    @abstractmethod
    def get_transactions(self) -> list[BrokerTransaction]:
        pass