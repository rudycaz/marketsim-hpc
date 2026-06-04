#!/bin/bash

TICKERS=(
    CVX
    RKLB
    MU
    NVDA
    BA
    AAPL
    MSFT
    AMZN
    GOOGL
    META
    TSLA
    AMD
    XOM
    JPM
    WMT
)

HORIZONS=(
    week
    month
    year
    longterm
)

for TICKER in "${TICKERS[@]}"; do
    for HORIZON in "${HORIZONS[@]}"; do

        if [ "$HORIZON" = "week" ]; then
            SIMULATIONS=100000
        elif [ "$HORIZON" = "month" ]; then
            SIMULATIONS=250000
        elif [ "$HORIZON" = "year" ]; then
            SIMULATIONS=250000
        elif [ "$HORIZON" = "longterm" ]; then
            SIMULATIONS=100000
        else
            SIMULATIONS=100000
        fi

        echo "Submitting $TICKER $HORIZON with $SIMULATIONS simulations"
        sbatch cluster/slurm_forecast_gpu.sh "$TICKER" "$HORIZON" "$SIMULATIONS"

        sleep 1
    done
done

