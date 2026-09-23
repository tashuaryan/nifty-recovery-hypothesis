"""
Validates the raw NIFTY data: checks for missing/duplicate dates,
incorrect ordering, invalid OHLC values, and reports actual coverage.
Cleans the data and saves it to data/processed/nifty_clean.csv.
"""

import pandas as pd
import os

RAW_PATH = "data/raw/nifty_raw.csv"
CLEAN_PATH = "data/processed/nifty_clean.csv"


def load_raw_data(path=RAW_PATH):
    df = pd.read_csv(path, skiprows=[1, 2])  # yfinance multi-index header rows
    df.columns = ["Date", "Close", "High", "Low", "Open", "Volume"]
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def validate(df):
    report = {}

    # Duplicate dates
    report["duplicate_dates"] = df["Date"].duplicated().sum()

    # Correct ordering
    report["is_sorted"] = df["Date"].is_monotonic_increasing

    # Missing values
    report["missing_values"] = df[["Open", "High", "Low", "Close"]].isna().sum().to_dict()

    # Invalid OHLC (High should be >= Low, Open/Close should be within [Low, High])
    invalid_hl = (df["High"] < df["Low"]).sum()
    invalid_open = ((df["Open"] > df["High"]) | (df["Open"] < df["Low"])).sum()
    invalid_close = ((df["Close"] > df["High"]) | (df["Close"] < df["Low"])).sum()
    report["invalid_high_low"] = int(invalid_hl)
    report["invalid_open_range"] = int(invalid_open)
    report["invalid_close_range"] = int(invalid_close)

    # Zero or negative prices
    report["non_positive_prices"] = int((df[["Open", "High", "Low", "Close"]] <= 0).any(axis=1).sum())

    # Coverage
    report["date_min"] = df["Date"].min()
    report["date_max"] = df["Date"].max()
    report["n_rows"] = len(df)

    return report


def clean_data(df):
    df = df.drop_duplicates(subset="Date")
    df = df.sort_values("Date").reset_index(drop=True)
    df = df.dropna(subset=["Open", "High", "Low", "Close"])
    df = df[(df["High"] >= df["Low"])]
    df = df[(df[["Open", "High", "Low", "Close"]] > 0).all(axis=1)]
    return df


def save_clean_data(df, path=CLEAN_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved cleaned data to {path} ({len(df)} rows).")


if __name__ == "__main__":
    df = load_raw_data()
    report = validate(df)

    print("=== Validation Report ===")
    for k, v in report.items():
        print(f"{k}: {v}")

    clean_df = clean_data(df)
    save_clean_data(clean_df)