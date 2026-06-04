#!/bin/bash
#SBATCH --job-name=marketsim_batch
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:a100:1
#SBATCH --time=04:00:00
#SBATCH --mem=8G
#SBATCH --output=slurm-batch-%j.out
#SBATCH --error=slurm-batch-%j.err

echo "========================================"
echo "MarketSim HPC Batch Forecast Job"
echo "Node: $(hostname)"
echo "Started: $(date)"
echo "========================================"

source .venv/bin/activate

echo "GPU info:"
nvidia-smi

mkdir -p data/results

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
        fi

        echo "----------------------------------------"
        echo "Running forecast"
        echo "Ticker: $TICKER"
        echo "Horizon: $HORIZON"
        echo "Simulations: $SIMULATIONS"
        echo "Started: $(date)"
        echo "----------------------------------------"

        python -m cli.predict \
            --ticker "$TICKER" \
            --horizon "$HORIZON" \
            --simulations "$SIMULATIONS" \
            | tee "data/results/${TICKER}_${HORIZON}_${SIMULATIONS}.txt"

        echo "Finished $TICKER $HORIZON at $(date)"
        echo
    done
done

echo "========================================"
echo "Batch job finished: $(date)"
echo "========================================"
