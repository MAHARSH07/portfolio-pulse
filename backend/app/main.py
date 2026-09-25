from fastapi import FastAPI

app = FastAPI(
    title="PortfolioPulse API",
    description="Backend API for the PortfolioPulse investment intelligence platform.",
    version="0.1.0",
)


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