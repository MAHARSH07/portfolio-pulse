from sqlalchemy.orm import Session
from decimal import Decimal

from app.market_data.groww_market_data import (
    GrowwMarketDataProvider,
)
from app.market_data.yfinance_market_data import (
    YFinanceMarketDataProvider,
)
from app.repositories.portfolio_repository import get_holdings
from app.schemas.portfolio import Holding, Portfolio
from app.services.market_data_service import MarketDataService


def get_portfolio(db: Session) -> Portfolio:
    holding_models = get_holdings(db)

    symbols = [
        holding_model.symbol
        for holding_model in holding_models
    ]

    market_data_service = MarketDataService(
        primary_provider=GrowwMarketDataProvider(),
        fallback_provider=YFinanceMarketDataProvider(),
    )

    prices = market_data_service.get_prices(symbols)

    holdings = []

    for holding_model in holding_models:
        price_snapshot = prices.get(holding_model.symbol)

        current_price = (
            price_snapshot.price
            if price_snapshot is not None and price_snapshot.price is not None
            else Decimal("0.00")
        )

        holding = Holding(
            symbol=holding_model.symbol,
            company_name=holding_model.company_name,
            quantity=holding_model.quantity,
            average_price=holding_model.average_price,
            current_price=current_price,
        )

        holdings.append(holding)

    total_invested = sum(
        holding.invested_value
        for holding in holdings
    )

    total_current_value = sum(
        holding.current_value
        for holding in holdings
    )

    total_pnl = total_current_value - total_invested

    total_pnl_percentage = (
        ((total_pnl / total_invested) * Decimal("100")).quantize(
            Decimal("0.01")
        )
        if total_invested
        else Decimal("0.00")
    )

    return Portfolio(
        holdings=holdings,
        total_invested=total_invested,
        total_current_value=total_current_value,
        total_pnl=total_pnl,
        total_pnl_percentage=total_pnl_percentage,
    )