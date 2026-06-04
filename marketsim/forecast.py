from typing import Dict

from marketsim.config import validate_horizon
from marketsim.data_fetcher import fetch_price_history
from marketsim.features import compute_daily_returns, momentum_score, volatility_risk_score
from marketsim.monte_carlo import run_monte_carlo
from marketsim.scoring import compute_trend_score, label_from_score


def forecast_ticker(ticker: str, horizon: str, simulations: int = 100_000, seed: int = 42) -> Dict:
    config = validate_horizon(horizon)
    ticker = ticker.upper().strip()

    prices = fetch_price_history(ticker, period=config.lookback_period)
    current_price = float(prices["Close"].iloc[-1])
    daily_returns = compute_daily_returns(prices)

    sim = run_monte_carlo(
        current_price=current_price,
        daily_returns=daily_returns,
        trading_days=config.trading_days,
        simulations=simulations,
        seed=seed,
    )

    momentum = momentum_score(prices)
    risk = volatility_risk_score(daily_returns)
    trend_score = compute_trend_score(sim.probability_up, sim.expected_return, momentum, risk)

    return {
        "ticker": ticker,
        "horizon": horizon,
        "horizon_label": config.label,
        "simulations": simulations,
        "simulation": sim.to_dict(),
        "signals": {
            "momentum_score": momentum,
            "volatility_risk_score": risk,
        },
        "trend_score": trend_score,
        "label": label_from_score(trend_score),
        "disclaimer": "Educational research only. Not financial advice.",
    }
