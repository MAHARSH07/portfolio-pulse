from growwapi import GrowwAPI

from app.core.config import settings


def main():
    if not settings.groww_api_key:
        raise ValueError("Groww API key is not configured.")

    if not settings.groww_api_secret:
        raise ValueError("Groww API secret is not configured.")

    access_token = GrowwAPI.get_access_token(
        api_key=settings.groww_api_key,
        secret=settings.groww_api_secret,
    )

    groww = GrowwAPI(access_token)

    holdings_response = groww.get_holdings_for_user(timeout=5)
    holdings = holdings_response["holdings"]

    exchange_symbols = tuple(
        f"NSE_{holding['trading_symbol']}"
        for holding in holdings
    )

    print("Holdings found:", len(exchange_symbols))
    print("Request symbols:", exchange_symbols)

    ltp_response = groww.get_ltp(
        segment=groww.SEGMENT_CASH,
        exchange_trading_symbols=exchange_symbols,
    )

    print("LTP request: SUCCESS")
    print("Response type:", type(ltp_response).__name__)
    print("Response:", ltp_response)


if __name__ == "__main__":
    main()