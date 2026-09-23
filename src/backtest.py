"""
Simple event backtest: buy next day's open after a qualifying fall,
sell at the close N trading days after the event day. Costs applied.
Reports in-sample vs out-of-sample (split at OOS_SPLIT_DATE).
"""

import os
import numpy as np
import pandas as pd

from config import HOLDING_PERIODS, OOS_SPLIT_DATE, ENTRY_COST_BPS, EXIT_COST_BPS
from events import load_clean_data

EVENTS_PATH = "outputs/results/events.csv"
OUT_PATH = "outputs/results/backtest_summary.csv"


def run_trades(prices, event_dates, n):
    """One trade per event. Returns DataFrame of net returns."""
    cost = (ENTRY_COST_BPS + EXIT_COST_BPS) / 10000
    trades = []
    for d in event_dates:
        if d not in prices.index:
            continue
        i = prices.index.get_loc(d)
        entry_i, exit_i = i + 1, i + n
        if exit_i >= len(prices):
            continue  # not enough future data
        gross = prices["Close"].iloc[exit_i] / prices["Open"].iloc[entry_i] - 1
        trades.append({"Date": d, "gross": gross, "net": gross - cost})
    return pd.DataFrame(trades)


def summarize(trades, label, n):
    if trades.empty:
        return {"holding_days": n, "sample": label, "n_trades": 0}
    r = trades["net"]
    return {
        "holding_days": n,
        "sample": label,
        "n_trades": len(r),
        "mean_net_%": r.mean() * 100,
        "median_net_%": r.median() * 100,
        "win_rate_%": (r > 0).mean() * 100,
        "best_%": r.max() * 100,
        "worst_%": r.min() * 100,
    }


def run_backtest():
    prices = load_clean_data()
    if "Date" in prices.columns:
        prices = prices.set_index("Date")
    prices.index = pd.to_datetime(prices.index)

    ev = pd.read_csv(EVENTS_PATH)
    event_dates = pd.to_datetime(ev["Date"])
    split = pd.to_datetime(OOS_SPLIT_DATE)

    rows = []
    for n in HOLDING_PERIODS:
        t = run_trades(prices, event_dates, n)
        rows.append(summarize(t, "all", n))
        rows.append(summarize(t[t["Date"] < split], "in-sample", n))
        rows.append(summarize(t[t["Date"] >= split], "out-of-sample", n))

    out = pd.DataFrame(rows).round(3)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    out.to_csv(OUT_PATH, index=False)
    print("\n=== Backtest (net of costs) ===")
    print(out.to_string(index=False))
    print(f"\nSaved to {OUT_PATH}")


if __name__ == "__main__":
    run_backtest()