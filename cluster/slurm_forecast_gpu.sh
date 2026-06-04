#!/bin/bash
#SBATCH --job-name=marketsim
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:a100:1
#SBATCH --time=00:30:00
#SBATCH --mem=8G
#SBATCH --output=slurm-forecast-%x-%j.out
#SBATCH --error=slurm-forecast-%x-%j.err

TICKER=$1
HORIZON=$2
SIMULATIONS=$3

if [ -z "$TICKER" ] || [ -z "$HORIZON" ] || [ -z "$SIMULATIONS" ]; then
    echo "Usage: sbatch cluster/slurm_forecast_gpu.sh TICKER HORIZON SIMULATIONS"
    echo "Example: sbatch cluster/slurm_forecast_gpu.sh CVX month 100000"
    exit 1
fi

echo "========================================"
echo "MarketSim HPC Forecast"
echo "Ticker: $TICKER"
echo "Horizon: $HORIZON"
echo "Simulations: $SIMULATIONS"
echo "Node: $(hostname)"
echo "Started: $(date)"
echo "========================================"

source .venv/bin/activate

echo "GPU info:"
nvidia-smi

echo "Running forecast..."
python -m cli.predict --ticker "$TICKER" --horizon "$HORIZON" --simulations "$SIMULATIONS"

echo "========================================"
echo "Finished: $(date)"
echo "========================================"
