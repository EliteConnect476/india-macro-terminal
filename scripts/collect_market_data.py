"""
Collects daily market data from Yahoo Finance. This is the EASIEST and
most reliable collector — Yahoo Finance has a stable, well-maintained
Python library (yfinance), unlike government websites which change
their page layouts without warning.

Run this daily. It fetches the latest closing price for each ticker.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from utils import save_observation
import yfinance as yf
from datetime import date

TICKERS = {
    "NIFTY_50": "^NSEI",
    "USD_INR": "INR=X",
    "GOLD_USD": "GC=F",
    "CRUDE_OIL_USD": "CL=F",
    "INDIA_VIX": "^INDIAVIX",
}

OUTPUT_FILE = "data/processed/market_data.csv"


def run():
    today = date.today().isoformat()
    for indicator, ticker in TICKERS.items():
        try:
            data = yf.Ticker(ticker).history(period="1d")
            if data.empty:
                print(f"[skip] No data returned for {indicator} ({ticker})")
                continue
            latest_close = float(data["Close"].iloc[-1])
            saved = save_observation(
                filepath=OUTPUT_FILE,
                date=today,
                indicator=indicator,
                value=round(latest_close, 2),
                unit="price",
                release_date=today,
                source="Yahoo Finance",
            )
            status = "saved" if saved else "already up to date"
            print(f"[{status}] {indicator}: {latest_close:.2f}")
        except Exception as e:
            print(f"[error] {indicator} ({ticker}): {e}")


if __name__ == "__main__":
    run()
