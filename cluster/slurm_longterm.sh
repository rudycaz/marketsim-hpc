#!/bin/bash
#SBATCH --job-name=marketsim_longterm
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=8
#SBATCH --time=04:00:00
#SBATCH --mem=64G
#SBATCH --output=slurm-%j.out

set -euo pipefail

TICKER=${1:-CVX}
SIMULATIONS=${2:-500000}

module load python || true
module load openmpi || true
source .venv/bin/activate

mpirun python -m cluster.monte_carlo_mpi --ticker "$TICKER" --horizon longterm --simulations "$SIMULATIONS"
