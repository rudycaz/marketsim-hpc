#!/usr/bin/env python3
import argparse
import hashlib
import json
import random


SUPPORTED_RANGES = {
    "week": 5,
    "month": 21,
    "year": 252,
    "5+ years": 1260,
}

RANGE_ALIASES = {
    "week": "week",
    "month": "month",
    "year": "year",
    "5+ years": "5+ years",
    "5+years": "5+ years",
    "5years": "5+ years",
    "5y": "5+ years",
}


def normalize_range(value: str) -> str:
    key = value.strip().lower()
    if key not in RANGE_ALIASES:
        raise ValueError(
            f"Unsupported range '{value}'. Supported ranges: {', '.join(SUPPORTED_RANGES)}"
        )
    return RANGE_ALIASES[key]


def simulate_price_series(ticker: str, time_range: str) -> list[float]:
    days = SUPPORTED_RANGES[time_range]
    seed = int(hashlib.sha256(f"{ticker.upper()}|{time_range}".encode()).hexdigest()[:16], 16)
    rng = random.Random(seed)
    drift = ((sum(ord(ch) for ch in ticker.upper()) % 11) - 5) / 10000
    volatility = 0.012

    prices = [100.0]
    for _ in range(days):
        daily_return = rng.gauss(drift, volatility)
        prices.append(round(prices[-1] * (1 + daily_return), 2))
    return prices


def predict_trend(prices: list[float]) -> str:
    if len(prices) < 2:
        return "sideways"
    change_pct = (prices[-1] - prices[0]) / prices[0]
    if change_pct > 0.02:
        return "upward"
    if change_pct < -0.02:
        return "downward"
    return "sideways"


def run_simulation(ticker: str, selected_range: str) -> dict[str, object]:
    normalized = normalize_range(selected_range)
    prices = simulate_price_series(ticker, normalized)
    trend = predict_trend(prices)
    change_pct = abs((prices[-1] - prices[0]) / prices[0])
    confidence = round(min(0.95, max(0.5, change_pct * 4)), 2)
    return {
        "ticker": ticker.upper(),
        "range": normalized,
        "trading_days": SUPPORTED_RANGES[normalized],
        "predicted_trend": trend,
        "confidence": confidence,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Predict stock trend for a ticker over week/month/year/5+ years."
    )
    parser.add_argument("ticker", help="Stock ticker symbol, e.g. AAPL")
    parser.add_argument(
        "--range",
        default="month",
        help="Time range: week, month, year, or 5+ years",
    )
    args = parser.parse_args()

    result = run_simulation(args.ticker, args.range)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
