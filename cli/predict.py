import argparse
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from marketsim.forecast import forecast_ticker


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def money(value: float) -> str:
    return f"${value:,.2f}"


def main() -> None:
    parser = argparse.ArgumentParser(description="MarketSim HPC stock trend forecast")
    parser.add_argument("--ticker", required=True, help="Stock ticker, e.g. CVX")
    parser.add_argument("--horizon", required=True, choices=["week", "month", "year", "longterm"])
    parser.add_argument("--simulations", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--json", action="store_true", help="Print raw JSON")
    parser.add_argument("--save", action="store_true", help="Save result to data/results/")
    args = parser.parse_args()

    result = forecast_ticker(args.ticker, args.horizon, args.simulations, args.seed)

    if args.save:
        Path("data/results").mkdir(parents=True, exist_ok=True)
        out = Path("data/results") / f"{result['ticker']}_{args.horizon}_{args.simulations}.json"
        out.write_text(json.dumps(result, indent=2))

    if args.json:
        print(json.dumps(result, indent=2))
        return

    sim = result["simulation"]
    print("=" * 60)
    print("MarketSim HPC Forecast")
    print("=" * 60)
    print(f"Ticker:            {result['ticker']}")
    print(f"Horizon:           {result['horizon_label']}")
    print(f"Simulations:       {result['simulations']:,}")
    print(f"Current Price:     {money(sim['current_price'])}")
    print(f"Expected Price:    {money(sim['expected_price'])}")
    print(f"Median Price:      {money(sim['median_price'])}")
    print(f"5%-95% Range:      {money(sim['p05_price'])} - {money(sim['p95_price'])}")
    print(f"Probability Up:    {pct(sim['probability_up'])}")
    print(f"Expected Return:   {pct(sim['expected_return'])}")
    print(f"Median Return:     {pct(sim['median_return'])}")
    print(f"5%-95% Return:     {pct(sim['p05_return'])} - {pct(sim['p95_return'])}")
    print(f"Momentum Score:    {result['signals']['momentum_score']:.1f}/100")
    print(f"Risk Score:        {result['signals']['volatility_risk_score']:.1f}/100")
    print(f"Trend Score:       {result['trend_score']:.1f}/100")
    print(f"Label:             {result['label']}")
    print("=" * 60)
    print("Educational research only. Not financial advice.")


if __name__ == "__main__":
    main()
