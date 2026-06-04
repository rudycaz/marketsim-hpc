import numpy as np
import pandas as pd


def compute_daily_returns(price_df: pd.DataFrame) -> np.ndarray:
    closes = price_df["Close"].astype(float)
    returns = closes.pct_change().dropna()
    returns = returns.replace([np.inf, -np.inf], np.nan).dropna()
    if returns.empty:
        raise ValueError("Not enough price history to compute returns.")
    return returns.to_numpy(dtype=float)


def momentum_score(price_df: pd.DataFrame) -> float:
    """Return a simple 0-100 momentum score using moving averages."""
    close = price_df["Close"].astype(float)
    if len(close) < 200:
        return 50.0

    last = close.iloc[-1]
    ma20 = close.rolling(20).mean().iloc[-1]
    ma50 = close.rolling(50).mean().iloc[-1]
    ma200 = close.rolling(200).mean().iloc[-1]

    score = 50.0
    if last > ma20:
        score += 10
    else:
        score -= 10
    if ma20 > ma50:
        score += 10
    else:
        score -= 10
    if ma50 > ma200:
        score += 15
    else:
        score -= 15
    if last > ma200:
        score += 15
    else:
        score -= 15

    return float(max(0, min(100, score)))


def volatility_risk_score(daily_returns: np.ndarray) -> float:
    """Return a 0-100 score where higher is lower risk."""
    annualized_vol = float(np.std(daily_returns) * np.sqrt(252))
    # Basic mapping: <=15% vol is high score, >=60% vol is low score.
    score = 100 - ((annualized_vol - 0.15) / (0.60 - 0.15)) * 100
    return float(max(0, min(100, score)))
