from datetime import date, timedelta
from utils import fetch_historical_data


# Use this for more long term trend
def calculate_sma(prices, window):
    """Calculate Simple Moving Average."""
    return prices.rolling(window=window).mean()


# Use this for scalping as its more precise
def calculate_ema(prices, window):
    """Calculate Exponential Moving Average."""
    return prices.ewm(span=window, adjust=False).mean()


# TODO: Check global trend for week/month/4h/day so that its not blocking for days
# TODO: Adjust entry points around EMA
def check_trend(df, index=None):
    """Determine the trend based on EMAs; Index is used for backtesting."""
    # Default EMA windows
    short_window = 9
    long_window = 25

    if index is not None and index < long_window:
        # Not enough data for analysis if a specific index is provided and is less than the long window
        return "NEUTRAL"

    # Select data up to the specified index if provided, otherwise use the full DataFrame
    data_to_use = df["close"][:index] if index is not None else df["close"]

    # Calculate EMAs
    short_ema = calculate_ema(data_to_use, short_window)
    long_ema = calculate_ema(data_to_use, long_window)

    # Determine trend based on the last values of EMAs
    if short_ema.iloc[-1] > long_ema.iloc[-1]:
        return "BULLISH"
    elif short_ema.iloc[-1] < long_ema.iloc[-1]:
        return "BEARISH"
    else:
        return "NEUTRAL"
