# Development Plan

Decisions (confirmed 2026-10-03):
- Data: read mdfeed's raw files through a `MarketSource` adapter; run a longer mdfeed capture (days) in parallel. Swap to mdfeed's `window()` API / database when it exists.
- Target (stage 0): log-return of mid-price 60 s ahead, features from 1 s bars.
- Goal: reasonable accuracy and stability, with an accepted error band so we do not overfit.
- Web app: Streamlit.
- Predictions stored locally in SQLite.

## Layout
```
pricer/
  CLAUDE.md, notes/            # DEV-notes.md, DEV-plan.md, findings/
  .claude/agents/              # scientist.md, project-manager.md, product-manager.md
  src/pricer/
    config.py
    sources/                   # MarketSource interface; MdfeedFileSource (raw spike/jsonl files)
    bars.py                    # events -> 1 s bars: mid, EMA-mid, spread, volume, signed flow
    features/                  # simple explainable factors, causal only
    models/                    # fit/predict interface: random walk, linear/ridge, RF/XGBoost
    evaluate/                  # walk-forward splits + embargo, metrics, statistical report
    pipeline/                  # resumable runner with checkpoint; backfill replays live path
    store/                     # SQLite predictions
    web/                       # Streamlit app
  tests/
```

## Milestones
1. **Scaffold** — venv, pyproject, CLAUDE.md, notes, agents.
2. **Source + bars** — read mdfeed raw files (`<recv_ns> <json>` lines), normalize, build 1 s bars. Tests on spike data.
3. **Leakage guardrails** — causal feature contract, future-perturbation test, walk-forward splits with embargo >= horizon.
4. **Evaluation** — physics-inspired models as starting points (random walk only as a reference line); directional (hit rate, binomial test, large-move hit rate) and absolute (MAE/RMSE in bps vs baseline, Diebold-Mariano, interval coverage). Exportable report.
5. **Stage 0 models** — linear/ridge on factors (EMA-mid deviation, multi-window returns, realized vol, trade-flow imbalance, book imbalance, spread).
6. **Prediction pipeline** — incremental, stoppable, resumable, backfill; writes SQLite.
7. **Streamlit app** — feed, current prediction with interval, rolling accuracy vs baseline, risk panel.
8. **Stage 1** — RF / gradient boosting, robust losses, resampling against outliers.
9. **Stage 2** — cross-ticker / cross-exchange (depends on mdfeed).
Scientist + project-manager review at the end of each milestone; findings go to `notes/findings/`.

## Risks / open items
- Data volume: only ~35 min of spike data in mdfeed so far; meaningful testing needs days.
- mdfeed raw format will change when its ingestion/storage milestones land; isolate it in `sources/`.
- 1-minute returns are noisy; expect small edges and wide error bands. Disclose this.
- 2026-10-03: user asked for an early playground on the spike data (few simple models + Streamlit view of a 10-minute window of 1-min-ahead predictions) before mdfeed matures.
