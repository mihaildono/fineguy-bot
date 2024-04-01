import pandas as pd
from client import binance_client
from datetime import date, timedelta


def get_top_20_symbols():
    """Get the top 20 symbols by 24h trading volume."""
    tickers = binance_client.get_ticker()
    # Sort the tickers by 24h volume in descending order and filter out non-USDT pairs for simplicity
    sorted_tickers = sorted(
        tickers, key=lambda x: float(x["quoteVolume"]), reverse=True
    )
    top_20_symbols = [
        ticker["symbol"] for ticker in sorted_tickers if "USDT" in ticker["symbol"]
    ][:20]
    return top_20_symbols


def fetch_historical_data(symbol, start_date, end_date):
    """Fetch historical price data for a symbol."""
    # 5m intervals for scalping
    klines = binance_client.get_historical_klines(symbol, "5m", start_date, end_date)
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
    # Convert 'open_time' to datetime format
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    return df


def get_df(symbol):
    """Fetch historical data for a symbol for the past 35 days."""
    end_date = date.today()
    start_date = end_date - timedelta(days=35)
    return fetch_historical_data(symbol, start_date, end_date)


def get_backtest_data():
    """Returns a dictionary of backtest data for multiple symbols."""
    return [
        {
            "symbol": "BTCUSDT",
            "start_date": "2023-10-01",
            "end_date": "2023-12-31",
            "trend": "BULLISH",
        },
        {
            "symbol": "ETHUSDT",
            "start_date": "2023-10-01",
            "end_date": "2023-12-31",
            "trend": "BULLISH",
        },
    ]
