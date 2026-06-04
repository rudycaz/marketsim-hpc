from dataclasses import dataclass, asdict
from typing import Dict

import numpy as np


@dataclass
class SimulationResult:
    simulations: int
    trading_days: int
    current_price: float
    expected_price: float
    median_price: float
    p05_price: float
    p95_price: float
    probability_up: float
    expected_return: float
    median_return: float
    p05_return: float
    p95_return: float

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


def run_monte_carlo(
    current_price: float,
    daily_returns: np.ndarray,
    trading_days: int,
    simulations: int,
    seed: int = 42,
    chunk_size: int = 100_000,
) -> SimulationResult:
    """Run Monte Carlo future price simulation using bootstrapped historical returns.

    The simulation samples historical daily returns with replacement and compounds them.
    This avoids assuming that returns are normally distributed.
    """
    if simulations <= 0:
        raise ValueError("simulations must be greater than zero")
    if trading_days <= 0:
        raise ValueError("trading_days must be greater than zero")

    rng = np.random.default_rng(seed)
    endings = []
    remaining = simulations

    while remaining > 0:
        n = min(chunk_size, remaining)
        sampled = rng.choice(daily_returns, size=(n, trading_days), replace=True)
        paths = current_price * np.cumprod(1.0 + sampled, axis=1)
        endings.append(paths[:, -1])
        remaining -= n

    final_prices = np.concatenate(endings)
    final_returns = (final_prices - current_price) / current_price

    return SimulationResult(
        simulations=int(simulations),
        trading_days=int(trading_days),
        current_price=float(current_price),
        expected_price=float(np.mean(final_prices)),
        median_price=float(np.median(final_prices)),
        p05_price=float(np.percentile(final_prices, 5)),
        p95_price=float(np.percentile(final_prices, 95)),
        probability_up=float(np.mean(final_prices > current_price)),
        expected_return=float(np.mean(final_returns)),
        median_return=float(np.median(final_returns)),
        p05_return=float(np.percentile(final_returns, 5)),
        p95_return=float(np.percentile(final_returns, 95)),
    )
