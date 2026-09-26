from growwapi import GrowwAPI

from app.core.config import settings
from app.schemas.broker import BrokerHolding


class GrowwClient:

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
    ):
        key = api_key or settings.groww_api_key
        secret = api_secret or settings.groww_api_secret

        if not key:
            raise ValueError(
                "Groww API key is not configured."
            )

        if not secret:
            raise ValueError(
                "Groww API secret is not configured."
            )

        access_token = GrowwAPI.get_access_token(
            api_key=key,
            secret=secret,
        )

        self.client = GrowwAPI(access_token)

    def get_user_profile(self):
        return self.client.get_user_profile()

    def get_holdings(self) -> list[BrokerHolding]:
        response = self.client.get_holdings_for_user(
            timeout=5
        )

        holdings_data = response["holdings"]

        return [
            BrokerHolding(
                symbol=item["trading_symbol"],
                isin=item["isin"],
                quantity=item["quantity"],
                average_price=item["average_price"],
            )
            for item in holdings_data
        ]