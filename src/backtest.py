"""
Event-driven backtest: buy next day's open after a qualifying fall, sell at
the close N trading days after the event day. One position at a time.
Reports trade statistics (in-sample / out-of-sample) and a daily
mark-to-market equity curve with max drawdown, vs buy-and-hold.
Cash earns 0% while flat.
"""

import os
import numpy as np
import pandas as pd

from config import HOLDING_PERIODS, OOS_SPLIT_DATE, ENTRY_COST_BPS, EXIT_COST_BPS
from events import load_clean_data

EVENTS_PATH = "outputs/results/events.csv"
OUT_PATH = "outputs/results/backtest_summary.csv"
EQUITY_SUMMARY_PATH = "outputs/results/backtest_equity_summary.csv"
CURVE_PATH = "outputs/results/equity_curve_{n}d.csv"
FIG_PATH = "outputs/figures/equity_curves.png"

ENTRY_COST = ENTRY_COST_BPS / 10000
EXIT_COST = EXIT_COST_BPS / 10000


def run_trades(prices, event_dates, n):
    """One trade per event, sequential (skip if entry is before previous exit)."""
    trades, last_exit_i = [], -1
    for d in sorted(event_dates):
        if d not in prices.index:
            continue
        i = prices.index.get_loc(d)
        entry_i, exit_i = i + 1, i + n
        if exit_i >= len(prices) or entry_i <= last_exit_i:
            continue
        gross = prices["Close"].iloc[exit_i] / prices["Open"].iloc[entry_i] - 1
        trades.append({
            "Date": d, "entry_i": entry_i, "exit_i": exit_i,
            "gross": gross, "net": gross - ENTRY_COST - EXIT_COST,
        })
        last_exit_i = exit_i
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
        "std_net_%": r.std() * 100,
        "win_rate_%": (r > 0).mean() * 100,
        "best_%": r.max() * 100,
        "worst_%": r.min() * 100,
    }


def build_equity(prices, trades):
    """Daily mark-to-market returns while in a trade; 0% while flat."""
    opens, closes = prices["Open"], prices["Close"]
    daily = pd.Series(0.0, index=prices.index)
    in_pos = pd.Series(False, index=prices.index)
    for _, t in trades.iterrows():
        e, x = int(t["entry_i"]), int(t["exit_i"])
        for k in range(e, x + 1):
            base = opens.iloc[e] if k == e else closes.iloc[k - 1]
            r = closes.iloc[k] / base - 1
            if k == e:
                r -= ENTRY_COST
            if k == x:
                r -= EXIT_COST
            daily.iloc[k] = r
            in_pos.iloc[k] = True
    equity = (1 + daily).cumprod()
    return equity, in_pos


def curve_stats(equity, years):
    dd = equity / equity.cummax() - 1
    return {
        "total_return_%": (equity.iloc[-1] - 1) * 100,
        "cagr_%": (equity.iloc[-1] ** (1 / years) - 1) * 100,
        "max_drawdown_%": dd.min() * 100,
    }


def run_backtest():
    prices = load_clean_data()
    if "Date" in prices.columns:
        prices = prices.set_index("Date")
    prices.index = pd.to_datetime(prices.index)

    ev = pd.read_csv(EVENTS_PATH)
    event_dates = list(pd.to_datetime(ev["Date"]))
    split = pd.to_datetime(OOS_SPLIT_DATE)
    years = (prices.index[-1] - prices.index[0]).days / 365.25

    # Buy-and-hold benchmark over the same period
    bh_equity = (1 + prices["Close"].pct_change().fillna(0)).cumprod()
    bh = curve_stats(bh_equity, years)

    trade_rows, equity_rows, curves = [], [], {}
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    for n in HOLDING_PERIODS:
        t = run_trades(prices, event_dates, n)
        trade_rows.append(summarize(t, "all", n))
        trade_rows.append(summarize(t[t["Date"] < split], "in-sample", n))
        trade_rows.append(summarize(t[t["Date"] >= split], "out-of-sample", n))

        equity, in_pos = build_equity(prices, t)
        curves[n] = equity
        stats = curve_stats(equity, years)
        equity_rows.append({
            "strategy": f"events, hold {n}d",
            "n_trades": len(t),
            "time_in_market_%": in_pos.mean() * 100,
            **stats,
        })
        pd.DataFrame({
            "Date": prices.index,
            "equity": equity.values,
            "buy_hold_equity": bh_equity.values,
            "drawdown_%": ((equity / equity.cummax() - 1) * 100).values,
        }).to_csv(CURVE_PATH.format(n=n), index=False)

    equity_rows.append({
        "strategy": "buy and hold NIFTY",
        "n_trades": 1,
        "time_in_market_%": 100.0,
        **bh,
    })

    trade_out = pd.DataFrame(trade_rows).round(3)
    equity_out = pd.DataFrame(equity_rows).round(3)
    trade_out.to_csv(OUT_PATH, index=False)
    equity_out.to_csv(EQUITY_SUMMARY_PATH, index=False)

    print("\n=== Backtest trades (net of costs) ===")
    print(trade_out.to_string(index=False))
    print("\n=== Equity curve summary (daily mark-to-market, cash = 0%) ===")
    print(equity_out.to_string(index=False))
    print(f"\nSaved to {OUT_PATH} and {EQUITY_SUMMARY_PATH}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        os.makedirs(os.path.dirname(FIG_PATH), exist_ok=True)
        fig, ax = plt.subplots(figsize=(10, 5))
        for n, eq in curves.items():
            ax.plot(eq.index, eq.values, label=f"events, hold {n}d")
        ax.plot(bh_equity.index, bh_equity.values, "k--", label="buy and hold")
        ax.set_yscale("log")
        ax.set_title("Equity curves (net of costs, log scale)")
        ax.legend()
        fig.savefig(FIG_PATH, dpi=150, bbox_inches="tight")
        print(f"Saved chart to {FIG_PATH}")
    except ImportError:
        print("matplotlib not installed, skipped chart.")


if __name__ == "__main__":
    run_backtest()