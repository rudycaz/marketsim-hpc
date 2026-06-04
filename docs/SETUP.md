# Full Setup Guide

This guide uses two environments:

- **Mac terminal**: your local computer for development, GitHub work, testing, and the dashboard.
- **Cluster terminal**: your school HPC login node for creating the environment and submitting SLURM jobs.

## 1. Create the GitHub repository

### Mac terminal

```bash
mkdir marketsim-hpc
cd marketsim-hpc
git init
```

Create a new empty GitHub repository named `marketsim-hpc`, then connect it:

```bash
git remote add origin git@github.com:<your-username>/marketsim-hpc.git
```

If you use HTTPS instead:

```bash
git remote add origin https://github.com/<your-username>/marketsim-hpc.git
```

## 2. Create local Python environment

### Mac terminal

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Run a local forecast

### Mac terminal

```bash
python cli/predict.py --ticker CVX --horizon month --simulations 100000
```

Try other horizons:

```bash
python cli/predict.py --ticker AAPL --horizon week --simulations 100000
python cli/predict.py --ticker MSFT --horizon year --simulations 100000
python cli/predict.py --ticker XOM --horizon longterm --simulations 50000
```

## 4. Run tests

### Mac terminal

```bash
pytest -v
```

## 5. Run the FastAPI backend

### Mac terminal

```bash
uvicorn backend.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## 6. Run the frontend

### Mac terminal

In a second terminal:

```bash
cd frontend
python3 -m http.server 3000
```

Open:

```text
http://127.0.0.1:3000
```

## 7. Push to GitHub

### Mac terminal

```bash
git add .
git commit -m "Initial MarketSim HPC project scaffold"
git branch -M main
git push -u origin main
```

## 8. Clone on the cluster

### Cluster terminal

```bash
git clone git@github.com:<your-username>/marketsim-hpc.git
cd marketsim-hpc
```

Or HTTPS:

```bash
git clone https://github.com/<your-username>/marketsim-hpc.git
cd marketsim-hpc
```

## 9. Set up Python on the cluster

### Cluster terminal

```bash
module avail python
module load python
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

If `mpi4py` fails, load MPI first:

```bash
module avail mpi
module load openmpi
pip install mpi4py
```

## 10. Test a small cluster run interactively

### Cluster terminal

```bash
source .venv/bin/activate
python cli/predict.py --ticker CVX --horizon week --simulations 10000
```

## 11. Submit a SLURM job

### Cluster terminal

```bash
sbatch cluster/slurm_month.sh CVX 1000000
```

Check status:

```bash
squeue -u $USER
```

View output after it runs:

```bash
ls -lh data/results
cat data/results/CVX_month_1000000_mpi.json
```

## 12. Pull cluster results back to your Mac

### Mac terminal

Use your actual cluster username and hostname:

```bash
scp -r <username>@<cluster-host>:/path/to/marketsim-hpc/data/results ./data/
```

Then commit important result examples:

```bash
git add docs data/results/.gitkeep
git commit -m "Document cluster forecasting results"
git push
```

Do not commit huge output files unless they are small examples.
