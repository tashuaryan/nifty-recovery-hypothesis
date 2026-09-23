"""
Statistical evidence: are returns after big falls different from normal days?
For each holding period: mean, median, win rate, and a bootstrap test of
(event mean - baseline mean).
"""

import os
import numpy as np
import pandas as pd

from config import HOLDING_PERIODS
from events import (
    load_clean_data,
    compute_daily_returns,
    detect_events,
    exclude_overlaps,
    compute_forward_returns,
)

N_BOOT = 10000
SEED = 42
OUT_PATH = "outputs/results/stats_summary.csv"


def bootstrap_diff(ev, base, n_boot=N_BOOT, seed=SEED):
    """Bootstrap the difference in means (events - baseline)."""
    rng = np.random.default_rng(seed)
    diffs = np.empty(n_boot)
    for i in range(n_boot):
        e = rng.choice(ev, size=len(ev), replace=True)
        b = rng.choice(base, size=len(base), replace=True)
        diffs[i] = e.mean() - b.mean()
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    # two-sided p-value: how often the bootstrapped diff crosses zero
    p = 2 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return lo, hi, min(p, 1.0)


def run_stats():
    df = load_clean_data()
    df = compute_daily_returns(df)
    df = detect_events(df)
    df = exclude_overlaps(df, HOLDING_PERIODS)
    df = compute_forward_returns(df, HOLDING_PERIODS)

    event_rows = df[df["is_event_final"]]
    base_rows = df[~df["is_event"]]

    rows = []
    for n in HOLDING_PERIODS:
        col = f"fwd_return_{n}d"
        ev = event_rows[col].dropna().values
        base = base_rows[col].dropna().values
        lo, hi, p = bootstrap_diff(ev, base)
        rows.append({
            "holding_days": n,
            "n_events": len(ev),
            "event_mean_%": ev.mean() * 100,
            "event_median_%": np.median(ev) * 100,
            "event_win_rate_%": (ev > 0).mean() * 100,
            "baseline_mean_%": base.mean() * 100,
            "baseline_win_rate_%": (base > 0).mean() * 100,
            "diff_mean_%": (ev.mean() - base.mean()) * 100,
            "diff_CI95_low_%": lo * 100,
            "diff_CI95_high_%": hi * 100,
            "boot_p_value": p,
        })

    out = pd.DataFrame(rows).round(3)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    out.to_csv(OUT_PATH, index=False)

    print("\n=== Statistics: events vs baseline ===")
    print(out.T.to_string(header=False))
    print(f"\nSaved to {OUT_PATH}")


if __name__ == "__main__":
    run_stats()