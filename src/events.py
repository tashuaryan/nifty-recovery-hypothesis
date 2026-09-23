"""
Detects significant one-day falls in NIFTY and computes forward returns
for each configured holding period. Handles overlapping events per config.
"""

import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import EVENT_THRESHOLD, HOLDING_PERIODS, EXCLUDE_OVERLAPPING_EVENTS

CLEAN_PATH = "data/processed/nifty_clean.csv"
EVENTS_PATH = "outputs/results/events.csv"


def load_clean_data(path=CLEAN_PATH):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df


def compute_daily_returns(df):
    df["daily_return"] = df["Close"].pct_change()
    return df


def detect_events(df, threshold=EVENT_THRESHOLD):
    df["is_event"] = df["daily_return"] <= threshold
    return df


def exclude_overlaps(df, holding_periods):
    """
    If EXCLUDE_OVERLAPPING_EVENTS is True, drop events that fall within
    the max holding-period window of a prior event, to avoid double-counting.
    """
    if not EXCLUDE_OVERLAPPING_EVENTS:
        return df

    max_hold = max(holding_periods)
    event_indices = df.index[df["is_event"]].tolist()
    keep = []
    last_kept = -max_hold - 1

    for idx in event_indices:
        if idx - last_kept > max_hold:
            keep.append(idx)
            last_kept = idx

    df["is_event_final"] = False
    df.loc[keep, "is_event_final"] = True
    return df


def compute_forward_returns(df, holding_periods):
    for n in holding_periods:
        # Entry = next day's open after event day; exit = close N days after entry
        entry_price = df["Open"].shift(-1)
        exit_price = df["Close"].shift(-(1 + n))
        df[f"fwd_return_{n}d"] = (exit_price - entry_price) / entry_price
    return df


def build_events_table(df, holding_periods=HOLDING_PERIODS):
    events = df[df["is_event_final"]].copy()
    cols = ["Date", "daily_return"] + [f"fwd_return_{n}d" for n in holding_periods]
    events = events[cols].dropna()
    return events


def save_events(df, path=EVENTS_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} events to {path}.")


if __name__ == "__main__":
    df = load_clean_data()
    df = compute_daily_returns(df)
    df = detect_events(df)
    df = exclude_overlaps(df, HOLDING_PERIODS)
    df = compute_forward_returns(df, HOLDING_PERIODS)

    events = build_events_table(df)
    save_events(events)

    print("\n=== Event Summary ===")
    print(f"Total qualifying event days (before overlap filter): {df['is_event'].sum()}")
    print(f"Final events used (after overlap filter): {df['is_event_final'].sum()}")
    print(f"Events with complete forward-return data: {len(events)}")
    print("\nSample events:")
    print(events.head(10))