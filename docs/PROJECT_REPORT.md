# Project Report Outline

## Title

MarketSim HPC: A Parallel Stock Trend Forecasting Simulator Using Real Market Data

## 1. Introduction

Explain the goal: build a private research tool that forecasts possible stock price scenarios using historical data and high-performance computing.

## 2. Motivation

Explain why the cluster is useful: Monte Carlo simulation is embarrassingly parallel because each simulated future path can be computed independently.

## 3. System Architecture

```text
User Input
  ↓
CLI / Web Dashboard
  ↓
FastAPI Backend
  ↓
Data Fetcher
  ↓
Feature Engineering
  ↓
Monte Carlo Engine
  ↓
MPI + SLURM Cluster Jobs
  ↓
Result Aggregator
  ↓
Forecast Report
```

## 4. Data

Initial version:

- historical daily stock prices
- adjusted closing prices
- trading volume

Future version:

- macroeconomic indicators
- SEC fundamentals
- oil prices
- sector ETF movement
- options implied volatility

## 5. Forecast Method

Describe daily returns, bootstrapped Monte Carlo simulation, and score calculation.

## 6. Parallelization Strategy

Each MPI rank runs a portion of the simulations. Rank 0 gathers the ending prices and computes summary statistics.

## 7. Experiments

Example benchmark table:

| Ticker | Horizon | Simulations | Nodes | Tasks | Runtime |
|---|---|---:|---:|---:|---:|
| CVX | month | 100,000 | 1 | 1 | TBD |
| CVX | month | 1,000,000 | 2 | 16 | TBD |
| CVX | year | 1,000,000 | 4 | 32 | TBD |

## 8. Results

Include probability up, expected return, median return, price range, and trend score.

## 9. Limitations

State that market forecasts are uncertain and historical behavior does not guarantee future behavior.

## 10. Future Work

- Add SEC fundamentals
- Add FRED macro data
- Add options implied volatility
- Add sector comparison
- Add batch forecasting for top companies
- Add model evaluation against historical holdout periods
