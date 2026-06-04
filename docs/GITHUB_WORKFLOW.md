# GitHub Workflow

## Branch setup

Use `main` for stable code.

Create feature branches for major changes:

```bash
git checkout -b feature/backend-api
git checkout -b feature/mpi-simulation
git checkout -b feature/dashboard
git checkout -b feature/macro-data
```

## Normal workflow

### Mac terminal

```bash
git status
git add .
git commit -m "Add MPI Monte Carlo simulation"
git push origin feature/mpi-simulation
```

Then open a Pull Request on GitHub.

## Good commit messages

Use messages like:

```text
Add local Monte Carlo forecast CLI
Add yfinance historical price fetcher
Add MPI simulation script for SLURM
Add FastAPI forecast endpoint
Add dashboard forecast form
Document cluster setup workflow
```

## What not to commit

Do not commit:

- `.env`
- API keys
- `.venv/`
- huge cached datasets
- huge result files
- SLURM output logs

These are already included in `.gitignore`.

## Suggested issues to create

Create GitHub issues for:

1. Build local CLI forecast command
2. Add yfinance price history fetcher
3. Add Monte Carlo simulation engine
4. Add trend score calculation
5. Add MPI cluster simulation
6. Add SLURM scripts
7. Add FastAPI backend
8. Add web dashboard
9. Add top-company batch forecast
10. Add macroeconomic data signals
11. Add SEC fundamentals
12. Add project report and benchmark results

## Pull Request template

Use this PR format:

```md
## Summary
- What changed?

## Testing
- [ ] Ran local CLI forecast
- [ ] Ran pytest
- [ ] Ran cluster job

## Output
Paste example output here.

## Notes
Any limitations or next steps.
```
