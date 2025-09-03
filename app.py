import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Trending Stocks Dashboard", layout="wide")

st.title(" Trending Stock Market Dashboard")

# Sidebar for user input
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g. AAPL, TSLA, NVDA)", "AAPL")
period = st.sidebar.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "5y"])
interval = st.sidebar.selectbox("Select Interval", ["1d", "1wk", "1mo"])

# File path for saving data
data_path = Path("data/latest_data.csv")

# Download stock data
data = yf.download(ticker, period=period, interval=interval)

if not data.empty:
    # Flatten MultiIndex columns if needed
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = ["_".join([str(c) for c in col if c]).strip() for col in data.columns]

    # Save the latest data to CSV
    data_path.parent.mkdir(exist_ok=True)
    data.to_csv(data_path)

    # Show raw data
    st.subheader(f"Raw Data for {ticker}")
    st.dataframe(data.tail())

    # Candlestick chart
    st.subheader(f"{ticker} Candlestick Chart")

    # Get column names safely
    open_col = [c for c in data.columns if "Open" in c][0]
    high_col = [c for c in data.columns if "High" in c][0]
    low_col = [c for c in data.columns if "Low" in c][0]
    close_col = [c for c in data.columns if "Close" in c][0]

    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data[open_col],
        high=data[high_col],
        low=data[low_col],
        close=data[close_col]
    )])
    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    # Moving averages
    st.subheader("Moving Averages (20 & 50 periods)")
    data['MA20'] = data[close_col].rolling(20).mean()
    data['MA50'] = data[close_col].rolling(50).mean()

    st.line_chart(data[[close_col, 'MA20', 'MA50']])

else:
    st.warning("No data found. Try another ticker.")
