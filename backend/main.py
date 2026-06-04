from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from marketsim.forecast import forecast_ticker

app = FastAPI(title="MarketSim HPC API", version="0.1.0")


class ForecastRequest(BaseModel):
    ticker: str = Field(..., examples=["CVX"])
    horizon: str = Field(..., examples=["month"])
    simulations: int = Field(100_000, ge=1000, le=10_000_000)
    seed: int = 42


@app.get("/")
def root():
    return {"name": "MarketSim HPC", "status": "running"}


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/forecast")
def forecast(request: ForecastRequest):
    try:
        return forecast_ticker(
            ticker=request.ticker,
            horizon=request.horizon,
            simulations=request.simulations,
            seed=request.seed,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
