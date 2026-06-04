# MarketSim HPC

Private stock trend forecasting research tool using real historical market data, Monte Carlo simulation, and HPC cluster execution.

> This project is for personal research and education. It does not provide financial advice and does not guarantee market outcomes.

## What it does

MarketSim HPC lets you enter a stock ticker such as `CVX`, select a forecast horizon, and run many simulated future price paths.

Supported horizons:

- `week`
- `month`
- `year`
- `longterm` for 5+ years

Example output:

```text
Ticker: CVX
Horizon: month
Simulations: 1,000,000
Probability Up: 56.82%
Expected Return: 1.94%
Median Return: 1.31%
5th Percentile Return: -7.42%
95th Percentile Return: 11.88%
Trend Score: 62/100
Label: Slightly Bullish
```

## Main features

- Real historical price data through `yfinance`
- Monte Carlo simulations using historical daily returns
- CLI forecast command
- MPI-based parallel simulation for cluster use
- SLURM job scripts
- FastAPI backend
- Simple local dashboard
- GitHub-ready documentation

## Quick start on Mac

```bash
git clone <your-repo-url> marketsim-hpc
cd marketsim-hpc
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python cli/predict.py --ticker CVX --horizon month --simulations 100000
```

## Quick start on cluster

```bash
git clone <your-repo-url> marketsim-hpc
cd marketsim-hpc
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
sbatch cluster/slurm_month.sh CVX 1000000
```

## Documentation

- [Full setup guide](docs/SETUP.md)
- [Cluster guide](docs/CLUSTER.md)
- [Model logic](docs/MODEL_LOGIC.md)
- [GitHub workflow](docs/GITHUB_WORKFLOW.md)
- [Project report outline](docs/PROJECT_REPORT.md)

## Project structure

```text
marketsim-hpc/
├── backend/              # FastAPI backend
├── cli/                  # Command-line tools
├── cluster/              # MPI and SLURM scripts
├── data/                 # Cached data and results
├── docs/                 # GitHub documentation
├── frontend/             # Simple local dashboard
├── marketsim/            # Core Python package
├── tests/                # Unit tests
├── requirements.txt
└── README.md
```

## Disclaimer

MarketSim HPC provides scenario-based probability estimates using historical data. It is not financial advice, not a trading bot, and not a guarantee of future returns.
