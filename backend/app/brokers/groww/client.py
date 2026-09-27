from growwapi import GrowwAPI
from decimal import Decimal

from app.core.config import settings
from app.schemas.broker import BrokerHolding
from app.schemas.instrument import BrokerInstrument

class GrowwClient:

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
    ):
        key = api_key or settings.groww_api_key
        secret = api_secret or settings.groww_api_secret

        if not key:
            raise ValueError("Groww API key is not configured.")

        if not secret:
            raise ValueError("Groww API secret is not configured.")

        access_token = GrowwAPI.get_access_token(
            api_key=key,
            secret=secret,
        )

        self.client = GrowwAPI(access_token)

    def get_user_profile(self):
        return self.client.get_user_profile()

    def get_instrument(
        self,
        trading_symbol: str,
        exchange: str = "NSE",
    ) -> BrokerInstrument:
        instrument = self.client.get_instrument_by_exchange_and_trading_symbol(
            exchange=exchange,
            trading_symbol=trading_symbol,
        )

        return BrokerInstrument(
            exchange=instrument["exchange"],
            exchange_token=str(instrument["exchange_token"]),
            trading_symbol=instrument["trading_symbol"],
            groww_symbol=instrument["groww_symbol"],
            name=instrument.get("name"),
            instrument_type=instrument["instrument_type"],
            segment=instrument["segment"],
            series=instrument.get("series"),
            isin=instrument.get("isin"),
            lot_size=(
                Decimal(str(instrument["lot_size"]))
                if instrument.get("lot_size") is not None
                else None
            ),
            tick_size=(
                Decimal(str(instrument["tick_size"]))
                if instrument.get("tick_size") is not None
                else None
            ),
        )

    def get_holdings(self) -> list[BrokerHolding]:
        response = self.client.get_holdings_for_user(timeout=5)

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
