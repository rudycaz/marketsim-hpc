# Cluster Guide

## Cluster vs Mac

Use the **Mac terminal** for writing code, testing small runs, editing docs, and pushing to GitHub.

Use the **cluster terminal** for large simulation jobs, MPI runs, and SLURM submissions.

## SLURM basics

Submit a job:

```bash
sbatch cluster/slurm_month.sh CVX 1000000
```

Check queue:

```bash
squeue -u $USER
```

Cancel a job:

```bash
scancel <job_id>
```

View output:

```bash
cat slurm-<job_id>.out
```

## Recommended first runs

Start small:

```bash
sbatch cluster/slurm_week.sh CVX 100000
```

Then medium:

```bash
sbatch cluster/slurm_month.sh CVX 1000000
```

Then long:

```bash
sbatch cluster/slurm_year.sh CVX 1000000
```

## Useful SLURM settings

```bash
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=8
#SBATCH --time=01:00:00
#SBATCH --mem=16G
```

Meaning:

- `--nodes`: number of cluster nodes
- `--ntasks-per-node`: MPI processes per node
- `--time`: maximum runtime
- `--mem`: memory requested

## How MPI is used

Each MPI task runs part of the total simulation count.

Example:

```text
1,000,000 simulations
32 MPI tasks
31,250 simulations per task
```

Rank 0 collects all ending prices, calculates final statistics, and writes a JSON result file.

## Common problems

### Problem: `mpi4py` will not install

Load MPI first:

```bash
module load openmpi
pip install mpi4py
```

### Problem: `module: command not found`

Your cluster may not use environment modules, or you may not be on the login node shell expected by the cluster. Check the school's cluster documentation.

### Problem: `mpirun: command not found`

Try:

```bash
module avail mpi
module load openmpi
which mpirun
```

### Problem: job stays pending

Check reason:

```bash
squeue -u $USER
```

If the job requests too many nodes, too much memory, or too much time, reduce those values.
