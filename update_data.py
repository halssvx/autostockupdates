# update_data.py
import yfinance as yf
import pandas as pd
from pathlib import Path

# Choose a default ticker list
tickers = ["AAPL", "TSLA", "NVDA", "MSFT", "AMZN"]

# Folder for data
data_path = Path("data")
data_path.mkdir(exist_ok=True)

for ticker in tickers:
    df = yf.download(ticker, period="6mo", interval="1d")
    file = data_path / f"{ticker}.csv"
    df.to_csv(file)
    print(f"Saved {ticker} data to {file}")
