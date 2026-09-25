from app.schemas.portfolio import Holding


MOCK_HOLDINGS = [
    Holding(
        symbol="KPIT",
        company_name="KPIT Technologies",
        quantity=10,
        average_price=900.00,
        current_price=950.00,
    ),
    Holding(
        symbol="INFY",
        company_name="Infosys",
        quantity=5,
        average_price=1500.00,
        current_price=1540.00,
    ),
    Holding(
        symbol="TCS",
        company_name="Tata Consultancy Services",
        quantity=3,
        average_price=3500.00,
        current_price=3420.00,
    ),
]