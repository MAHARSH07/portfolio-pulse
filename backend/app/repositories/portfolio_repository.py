from app.data.portfolio import MOCK_HOLDINGS
from app.schemas.portfolio import Holding


def get_holdings() -> list[Holding]:
    return MOCK_HOLDINGS