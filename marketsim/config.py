from dataclasses import dataclass


@dataclass(frozen=True)
class HorizonConfig:
    trading_days: int
    lookback_period: str
    label: str


HORIZONS = {
    "week": HorizonConfig(trading_days=5, lookback_period="2y", label="1 Week"),
    "month": HorizonConfig(trading_days=21, lookback_period="5y", label="1 Month"),
    "year": HorizonConfig(trading_days=252, lookback_period="10y", label="1 Year"),
    "longterm": HorizonConfig(trading_days=252 * 5, lookback_period="max", label="5+ Years"),
}


def validate_horizon(horizon: str) -> HorizonConfig:
    key = horizon.lower().strip()
    if key not in HORIZONS:
        valid = ", ".join(HORIZONS.keys())
        raise ValueError(f"Invalid horizon '{horizon}'. Valid options: {valid}")
    return HORIZONS[key]
