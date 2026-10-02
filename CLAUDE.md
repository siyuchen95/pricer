# pricer

Mid-frequency pricing models for BTCUSDC (Binance), fed by `~/code/mdfeed`. Read `notes/DEV-notes.md` (goals, habits) and `notes/DEV-plan.md` (decisions, layout, milestones) before working.

## Rules
- Use the venv: `.venv` (python3.12). Manage it with `python -m uv` (e.g. `python -m uv sync`, `python -m uv run pytest`).
- Simple code, limited comments, modular models behind one interface.
- Never future-peek: features at time t use data <= t only; strict train/test separation with an embargo. Every new feature or model needs a leakage test.
- Physics models (mean reversion, diffusion, driven motion) are inspiration for factors and models; the random walk is a reference line, not the yardstick.
- Read mdfeed data only through `pricer.sources`; never write into `~/code/mdfeed`.
- Keep notes in `notes/`. Never commit `data/` or `.env`.

## Agents (`.claude/agents/`)
- `scientist`: model-building process, statistics, explainability, code quality.
- `project-manager`: alignment with goals, overfitting risk, user view of the web app, disclosure, pace.
- `product-manager`: quick answers about the pricer without diving into details.
Scientist and project-manager are best friends: they trust and critically challenge each other.

## Commands
- Test: `python -m uv run pytest`
- Lint: `python -m uv run ruff check . && python -m uv run ruff format --check .`
