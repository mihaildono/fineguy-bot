from binance.client import Client
import pandas as pd
from client import binance_client
from datetime import date, timedelta


def fetch_historical_data(symbol, interval, start_date, end_date):
    """Fetch historical price data for a symbol."""
    klines = binance_client.get_historical_klines(
        symbol, interval, start_date, end_date
    )
    df = pd.DataFrame(
        klines,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
            "ignore",
        ],
    )
    df["close"] = pd.to_numeric(df["close"])
    return df


def calculate_sma(prices, window):
    """Calculate Simple Moving Average."""
    return prices.rolling(window=window).mean()


def check_trend(symbol):
    """Check the trend by comparing short-term SMA with long-term SMA."""
    now = date.today()
    initial_date = now - timedelta(days=35)  # Fetch data for the past 35 days
    df = fetch_historical_data(symbol, Client.KLINE_INTERVAL_1DAY, initial_date, now)
    df["sma_short"] = calculate_sma(df["close"], 7)  # 7-day SMA
    df["sma_long"] = calculate_sma(df["close"], 25)  # 25-day SMA

    # Check the latest values to determine the trend
    if df["sma_short"].iloc[-1] > df["sma_long"].iloc[-1]:
        return "BULLISH"
    elif df["sma_short"].iloc[-1] < df["sma_long"].iloc[-1]:
        return "BEARISH"
    else:
        return "NEUTRAL"


def check_trend_for_date(df, index, short_window=7, long_window=25):
    """Determine the trend for a specific date in the DataFrame based on SMAs."""
    if index < long_window:  # Not enough data for analysis
        return "NEUTRAL"

    # Calculate SMAs up to the current point
    short_sma = df["close"][:index].rolling(window=short_window).mean().iloc[-1]
    long_sma = df["close"][:index].rolling(window=long_window).mean().iloc[-1]

    # Determine trend
    if short_sma > long_sma:
        return "BULLISH"
    elif short_sma < long_sma:
        return "BEARISH"
    else:
        return "NEUTRAL"
