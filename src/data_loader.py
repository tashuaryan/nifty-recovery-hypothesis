"""
Fetches NIFTY 50 historical daily OHLC data from Yahoo Finance
and saves it as raw data (untouched) for later validation/cleaning.
"""

import yfinance as yf
import pandas as pd
import os

TICKER = "^NSEI"   # NIFTY 50 index ticker on Yahoo Finance
RAW_DATA_PATH = "data/raw/nifty_raw.csv"


def fetch_nifty_data(start_date="2000-01-01", end_date=None):
    """
    Downloads daily OHLC data for NIFTY 50 from Yahoo Finance.
    Returns a pandas DataFrame with Date, Open, High, Low, Close, Volume.
    """
    print(f"Fetching {TICKER} data from {start_date} to {end_date or 'today'}...")
    df = yf.download(TICKER, start=start_date, end=end_date, progress=False)

    if df.empty:
        raise ValueError("No data returned. Check ticker symbol or date range.")

    df.reset_index(inplace=True)
    return df


def save_raw_data(df, path=RAW_DATA_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved raw data to {path} ({len(df)} rows).")


if __name__ == "__main__":
    data = fetch_nifty_data(start_date="2000-01-01")
    save_raw_data(data)
    print(data.head())
    print(data.tail())
    print(f"Date range: {data['Date'].min()} to {data['Date'].max()}")
