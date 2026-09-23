"""
Robustness: vary the fall threshold and holding period.
Entry = next day's open, exit = close N days after event day, net of costs.
Overlapping events (within N days of the last accepted event) are skipped.
"""

import os
import pandas as pd

from config import OOS_SPLIT_DATE, ENTRY_COST_BPS, EXIT_COST_BPS
from events import load_clean_data

THRESHOLDS = [-0.015, -0.02, -0.025, -0.03]
HOLDS = [1, 3, 5, 10, 20]
OUT_PATH = "outputs/results/robustness_summary.csv"


def trades_for(prices, thr, n):
    cost = (ENTRY_COST_BPS + EXIT_COST_BPS) / 10000
    ret = prices["Close"].pct_change()
    idx = [i for i in range(1, len(prices)) if ret.iloc[i] <= thr]

    out, last = [], -10**9
    for i in idx:
        if i - last <= n:          # overlaps previous accepted event
            continue
        entry_i, exit_i = i + 1, i + n
        if exit_i >= len(prices):
            continue
        last = i
        gross = prices["Close"].iloc[exit_i] / prices["Open"].iloc[entry_i] - 1
        out.append({"Date": prices.index[i], "net": gross - cost})
    return pd.DataFrame(out)


def run_robustness():
    prices = load_clean_data()
    if "Date" in prices.columns:
        prices = prices.set_index("Date")
    prices.index = pd.to_datetime(prices.index)
    split = pd.to_datetime(OOS_SPLIT_DATE)

    rows = []
    for thr in THRESHOLDS:
        for n in HOLDS:
            t = trades_for(prices, thr, n)
            if t.empty:
                continue
            oos = t[t["Date"] >= split]["net"]
            rows.append({
                "threshold_%": thr * 100,
                "holding_days": n,
                "n_trades": len(t),
                "mean_net_%": t["net"].mean() * 100,
                "median_net_%": t["net"].median() * 100,
                "win_rate_%": (t["net"] > 0).mean() * 100,
                "worst_%": t["net"].min() * 100,
                "oos_n": len(oos),
                "oos_mean_%": oos.mean() * 100 if len(oos) else float("nan"),
            })

    out = pd.DataFrame(rows).round(3)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    out.to_csv(OUT_PATH, index=False)
    print("\n=== Robustness (net of costs) ===")
    print(out.to_string(index=False))
    print(f"\nSaved to {OUT_PATH}")


if __name__ == "__main__":
    run_robustness()