from growwapi import GrowwAPI

from app.core.config import settings


def test_groww_auth() -> None:
    if not settings.groww_api_key:
        raise ValueError("GROWW_API_KEY is not configured.")

    if not settings.groww_api_secret:
        raise ValueError("GROWW_API_SECRET is not configured.")

    try:
        access_token = GrowwAPI.get_access_token(
            api_key=settings.groww_api_key,
            secret=settings.groww_api_secret,
        )

        print("Groww authentication successful.")
        print("Access token generated:", bool(access_token))

    except Exception as exc:
        print("Groww authentication failed.")
        print("Error type:", type(exc).__name__)
        print("Error:", exc)


if __name__ == "__main__":
    test_groww_auth()