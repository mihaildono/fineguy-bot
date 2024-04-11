import pandas as pd
import numpy as np


def EMA(values, span):
    """Calculate the Exponential Moving Average (EMA) of a series of values."""
    return pd.Series(values).ewm(span=span, adjust=False).mean().bfill()


def SMA(values, span):
    """Calculate the Simple Moving Average (SMA) of a series of values."""
    return pd.Series(values).rolling(span).mean()


# TODO: we should take PSAR into account after 3 ticks
def PSAR(data, af_start=0.02, af_increment=0.02, af_max=0.2):
    """
    Calculates the Parabolic SAR for a dataset.

    Parameters:
    - data: DataFrame with 'High' and 'Low' price columns.
    - af_start: Initial value of the acceleration factor.
    - af_increment: Increment value for the acceleration factor.
    - af_max: Maximum value for the acceleration factor.

    Returns:
    - A pandas Series with the Parabolic SAR values.
    """
    high, low = data["High"], data["Low"]
    n = len(data)
    sar = pd.Series(data=np.nan, index=range(n))
    sar[0] = low[0]
    ep = high[0]
    af = af_start
    upward = True

    for i in range(1, n):
        if upward:
            sar[i] = sar[i - 1] + af * (ep - sar[i - 1])
            if high[i] > ep:
                ep = high[i]
                af = min(af + af_increment, af_max)
            if low[i] < sar[i]:
                upward = False
                sar[i] = ep
                ep = low[i]
                af = af_start
        else:
            sar[i] = sar[i - 1] + af * (ep - sar[i - 1])
            if low[i] < ep:
                ep = low[i]
                af = min(af + af_increment, af_max)
            if high[i] > sar[i]:
                upward = True
                sar[i] = ep
                ep = high[i]
                af = af_start

        if upward:
            sar[i] = min(sar[i], low[i], low[i - 1] if i > 0 else low[i])
        else:
            sar[i] = max(sar[i], high[i], high[i - 1] if i > 0 else high[i])

    return sar


def get_trend(close_price, ema, psar):
    """Determine the trend based on the EMA and PSAR indicators."""
    is_positive_trend = close_price > ema and close_price > psar
    is_negative_trend = close_price < ema and close_price < psar
    return is_positive_trend, is_negative_trend
