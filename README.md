# NIFTY Recovery Hypothesis

Research project: does the NIFTY 50 tend to recover after a significant
one-day fall, and is any such effect statistically meaningful and
tradeable after costs?

Full write-up: see `research_note.md`.

## Summary of findings
- Average forward returns after a -2% day are higher than on normal days
  at every horizon tested (1, 3, 5, 10 days), but the difference is not
  statistically significant (bootstrap p = 0.115 to 0.298, n = 101 events).
- After 20 bps round-trip costs, 10 to 20 day holds are positive in most
  settings; 1 to 5 day holds mostly are not.
- Results are sensitive to design choices (overlap handling, threshold)
  and carry severe tail risk (single trades down 20%+).
- This is a research investigation, not a validated trading strategy.

## Setup
1. Create and activate a virtual environment (Windows PowerShell):
       python -m venv venv
       venv\Scripts\activate
2. Install dependencies:
       pip install -r requirements.txt

## How to run (in this order)
    python src/data_loader.py     # download NIFTY 50 daily data (Yahoo Finance)
    python src/validation.py      # data quality checks, writes cleaned data
    python src/events.py          # detect events, forward returns
    python src/stats.py           # events vs baseline, bootstrap test
    python src/backtest.py        # net-of-cost trades, in/out-of-sample
    python src/robustness.py      # threshold and holding-period sweep

Results are saved to `outputs/results/`.

## Configuration
All parameters live in `src/config.py` (event threshold, holding periods,
out-of-sample split date, transaction costs, overlap handling). Change a
value there and re-run; no other code needs editing.

## Method in brief
- Event: close-to-close daily return <= threshold (default -2%).
- Entry: next trading day's open (no look-ahead bias).
- Exit: close N trading days after the event day.
- Overlapping events are excluded to avoid double counting.
- Costs: 10 bps per side, an assumed approximation.
- Out-of-sample: events on or after the split date in `config.py`.

## Limitations
Single index and event type, small out-of-sample sample (17 events),
assumed costs, no position sizing or risk controls, and 20 tested
parameter combinations create some data-mining risk.

## Data source
Yahoo Finance via the `yfinance` library (ticker ^NSEI).