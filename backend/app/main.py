from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.db.database import engine

from app.routers.portfolio import router as portfolio_router
from app.routers.transaction import router as transaction_router


app = FastAPI(
    title="PortfolioPulse API",
    description="Backend API for the PortfolioPulse investment intelligence platform.",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(portfolio_router)
app.include_router(transaction_router)


@app.get("/")
def root():
    return {
        "message": "PortfolioPulse API is running",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.get("/db-health")
def database_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception as exc:
        print(f"Database connection error: {exc}")

        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(exc),
        }