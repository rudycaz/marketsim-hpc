from pathlib import Path
from typing import Optional

import pandas as pd
import yfinance as yf

CACHE_DIR = Path("data/cached_prices")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def fetch_price_history(ticker: str, period: str = "5y", use_cache: bool = True) -> pd.DataFrame:
    """Fetch historical daily price data for a ticker.

    Uses yfinance for educational/private research use.
    """
    ticker = ticker.upper().strip()
    cache_path = CACHE_DIR / f"{ticker}_{period}.csv"

    if use_cache and cache_path.exists():
        df = pd.read_csv(cache_path, parse_dates=["Date"])
        if not df.empty:
            return df

    df = yf.download(ticker, period=period, interval="1d", auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError(f"No price history found for ticker '{ticker}'.")

    df = df.reset_index()

    # Flatten yfinance multi-index columns if needed.
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    required = {"Date", "Open", "High", "Low", "Close", "Volume"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing expected price columns: {sorted(missing)}")

    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]].dropna()
    if use_cache:
        df.to_csv(cache_path, index=False)
    return df
