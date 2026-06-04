import argparse
import json
from pathlib import Path

import numpy as np
from mpi4py import MPI

from marketsim.config import validate_horizon
from marketsim.data_fetcher import fetch_price_history
from marketsim.features import compute_daily_returns, momentum_score, volatility_risk_score
from marketsim.scoring import compute_trend_score, label_from_score


def split_work(total: int, size: int, rank: int) -> int:
    base = total // size
    extra = total % size
    return base + (1 if rank < extra else 0)


def main() -> None:
    parser = argparse.ArgumentParser(description="MPI Monte Carlo stock simulator")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--horizon", required=True, choices=["week", "month", "year", "longterm"])
    parser.add_argument("--simulations", type=int, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="data/results")
    args = parser.parse_args()

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        config = validate_horizon(args.horizon)
        ticker = args.ticker.upper().strip()
        prices = fetch_price_history(ticker, period=config.lookback_period)
        current_price = float(prices["Close"].iloc[-1])
        daily_returns = compute_daily_returns(prices)
        momentum = momentum_score(prices)
        risk = volatility_risk_score(daily_returns)
        payload = {
            "ticker": ticker,
            "trading_days": config.trading_days,
            "horizon_label": config.label,
            "current_price": current_price,
            "daily_returns": daily_returns,
            "momentum": momentum,
            "risk": risk,
        }
    else:
        payload = None

    payload = comm.bcast(payload, root=0)

    local_n = split_work(args.simulations, size, rank)
    rng = np.random.default_rng(args.seed + rank)
    sampled = rng.choice(payload["daily_returns"], size=(local_n, payload["trading_days"]), replace=True)
    ending_prices = payload["current_price"] * np.prod(1.0 + sampled, axis=1)

    gathered = comm.gather(ending_prices, root=0)

    if rank == 0:
        final_prices = np.concatenate(gathered)
        current = payload["current_price"]
        final_returns = (final_prices - current) / current
        probability_up = float(np.mean(final_prices > current))
        expected_return = float(np.mean(final_returns))
        trend_score = compute_trend_score(probability_up, expected_return, payload["momentum"], payload["risk"])

        result = {
            "ticker": payload["ticker"],
            "horizon": args.horizon,
            "horizon_label": payload["horizon_label"],
            "simulations": int(args.simulations),
            "mpi_tasks": int(size),
            "simulation": {
                "current_price": float(current),
                "expected_price": float(np.mean(final_prices)),
                "median_price": float(np.median(final_prices)),
                "p05_price": float(np.percentile(final_prices, 5)),
                "p95_price": float(np.percentile(final_prices, 95)),
                "probability_up": probability_up,
                "expected_return": expected_return,
                "median_return": float(np.median(final_returns)),
                "p05_return": float(np.percentile(final_returns, 5)),
                "p95_return": float(np.percentile(final_returns, 95)),
            },
            "signals": {
                "momentum_score": float(payload["momentum"]),
                "volatility_risk_score": float(payload["risk"]),
            },
            "trend_score": trend_score,
            "label": label_from_score(trend_score),
            "disclaimer": "Educational research only. Not financial advice.",
        }

        out_dir = Path(args.output)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{payload['ticker']}_{args.horizon}_{args.simulations}_mpi.json"
        out_path.write_text(json.dumps(result, indent=2))
        print(json.dumps(result, indent=2))
        print(f"Saved result to {out_path}")


if __name__ == "__main__":
    main()
