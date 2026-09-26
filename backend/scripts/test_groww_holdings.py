from growwapi import GrowwAPI

from app.core.config import settings


def main() -> None:
    if not settings.groww_api_key:
        raise ValueError("GROWW_API_KEY is not configured.")

    if not settings.groww_api_secret:
        raise ValueError("GROWW_API_SECRET is not configured.")

    try:
        access_token = GrowwAPI.get_access_token(
            api_key=settings.groww_api_key,
            secret=settings.groww_api_secret,
        )

        groww = GrowwAPI(access_token)

        response = groww.get_holdings_for_user(timeout=5)

        print("Holdings API call: SUCCESS")
        print("Response type:", type(response).__name__)

        if not isinstance(response, dict):
            print("Unexpected response type.")
            return

        print("Top-level keys:", list(response.keys()))

        payload = response.get("payload")

        if not isinstance(payload, dict):
            print("Payload is missing or is not a dictionary.")
            return

        print("Payload keys:", list(payload.keys()))

        holdings = payload.get("holdings")

        if not isinstance(holdings, list):
            print("Holdings is missing or is not a list.")
            return

        print("Number of holdings:", len(holdings))

        if holdings:
            first_holding = holdings[0]

            if isinstance(first_holding, dict):
                print(
                    "First holding keys:",
                    list(first_holding.keys()),
                )
            else:
                print(
                    "Unexpected holding item type:",
                    type(first_holding).__name__,
                )

    except Exception as exc:
        print("Holdings API call: FAILED")
        print("Error type:", type(exc).__name__)
        print("Error:", exc)


if __name__ == "__main__":
    main()