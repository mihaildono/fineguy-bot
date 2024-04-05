import pandas as pd


def EMA(values, span):
    """Calculate the Exponential Moving Average (EMA) of a series of values."""
    return pd.Series(values).ewm(span=span, adjust=False).mean().bfill()


def SMA(values, span):
    """Calculate the Simple Moving Average (SMA) of a series of values."""
    return pd.Series(values).rolling(span).mean()
