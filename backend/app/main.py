from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.portfolio import router as portfolio_router


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