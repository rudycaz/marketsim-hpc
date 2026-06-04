# Model Logic

MarketSim HPC is a probability and scenario tool, not a guarantee tool.

## Inputs

The first version uses:

- ticker symbol
- forecast horizon
- historical closing prices
- historical daily returns
- number of simulations

## Horizons

| Horizon | Trading Days | Main Use |
|---|---:|---|
| week | 5 | short-term movement |
| month | 21 | near-term trend |
| year | 252 | medium-term scenario |
| longterm | 1260 | 5+ year scenario |

## Daily return

```text
daily_return = (today_close - yesterday_close) / yesterday_close
```

## Monte Carlo method

1. Get historical daily returns.
2. Randomly sample returns with replacement.
3. Build possible future paths.
4. Repeat many times.
5. Analyze the distribution of final prices.

## Output statistics

- current price
- expected future price
- median future price
- 5th percentile price
- 95th percentile price
- probability price ends higher
- expected return
- median return
- trend score
- trend label

## Trend score

The current MVP score uses:

```text
45% simulation probability
25% expected return
20% momentum score
10% volatility risk score
```

## Labels

| Score | Label |
|---:|---|
| 81-100 | Strong Bullish |
| 61-80 | Bullish |
| 41-60 | Neutral |
| 21-40 | Bearish |
| 0-20 | Strong Bearish |

## Limitations

The MVP does not yet include:

- earnings data
- SEC fundamentals
- interest rates
- inflation
- oil prices
- options implied volatility
- news sentiment
- analyst estimates

Future versions should add these signals before treating the output as more serious research.
