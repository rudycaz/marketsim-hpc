#!/bin/bash
#SBATCH --job-name=marketsim_week_gpu
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:a100:1
#SBATCH --time=00:15:00
#SBATCH --mem=8G
#SBATCH --output=slurm-week-gpu-%j.out
#SBATCH --error=slurm-week-gpu-%j.err

TICKER=$1
SIMULATIONS=$2

echo "========================================"
echo "MarketSim HPC GPU Partition Forecast"
echo "Ticker: $TICKER"
echo "Simulations: $SIMULATIONS"
echo "Node: $(hostname)"
echo "Started: $(date)"
echo "========================================"

source .venv/bin/activate

echo "GPU info:"
nvidia-smi

echo "Running forecast..."
python -m cli.predict --ticker "$TICKER" --horizon week --simulations "$SIMULATIONS"

echo "========================================"
echo "Finished: $(date)"
echo "========================================"
