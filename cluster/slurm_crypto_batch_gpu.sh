#!/bin/bash
#SBATCH --job-name=marketsim_crypto
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:a100:1
#SBATCH --time=01:30:00
#SBATCH --mem=8G
#SBATCH --output=slurm-crypto-%j.out
#SBATCH --error=slurm-crypto-%j.err

echo "========================================"
echo "MarketSim HPC Crypto Forecast Job"
echo "Node: $(hostname)"
echo "Started: $(date)"
echo "========================================"

source .venv/bin/activate

echo "GPU info:"
nvidia-smi

mkdir -p data/results

ASSETS=(
    BTC
    ETH
    SOL
    XRP
    DOGE
    ADA
    AVAX
    LINK
    LTC
)

HORIZONS=(
    week
    month
    year
    longterm
)

for ASSET in "${ASSETS[@]}"; do
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
        echo "Running crypto forecast"
        echo "Asset: $ASSET"
        echo "Horizon: $HORIZON"
        echo "Simulations: $SIMULATIONS"
        echo "Started: $(date)"
        echo "----------------------------------------"

        python -m cli.predict \
            --ticker "$ASSET" \
            --horizon "$HORIZON" \
            --simulations "$SIMULATIONS" \
            --save \
            | tee "data/results/${ASSET}_${HORIZON}_${SIMULATIONS}.txt"

        echo "Finished $ASSET $HORIZON at $(date)"
        echo
    done
done

echo "========================================"
echo "Crypto batch job finished: $(date)"
echo "========================================"
