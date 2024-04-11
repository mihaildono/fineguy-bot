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


def fetch_historical_data(symbol, start_date, end_date, interval="5m", csv=False):
    """Fetch historical price data for a symbol and optionally save it as a CSV for backtesting."""
    # Example: fetch_historical_data("BTCUSDT", "2023-11-01", "2023-12-01", csv=True)
    # Usage: prices = pd.read_csv("data.csv", index_col="Date", parse_dates=True)
    klines = binance_client.get_historical_klines(
        symbol, interval, start_date, end_date
    )
    df = pd.DataFrame(
        klines,
        columns=[
            "Open_time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "Close_time",
            "Quote_asset_volume",
            "Number_of_trades",
            "Taker_buy_base_asset_volume",
            "Taker_buy_quote_asset_volume",
            "Ignore",
        ],
    )

    # Convert 'Open_time' to datetime format and set as index
    df["Date"] = pd.to_datetime(df["Open_time"], unit="ms")
    df.set_index("Date", inplace=True)

    # Drop unnecessary columns
    df.drop(
        columns=[
            "Open_time",
            "Close_time",
            "Quote_asset_volume",
            "Number_of_trades",
            "Taker_buy_base_asset_volume",
            "Taker_buy_quote_asset_volume",
            "Ignore",
        ],
        inplace=True,
    )

    # Format the DataFrame according to the screenshot: round to 8 decimal places for prices and volume
    df["Open"] = df["Open"].round(8)
    df["High"] = df["High"].round(8)
    df["Low"] = df["Low"].round(8)
    df["Close"] = df["Close"].round(8)
    df["Volume"] = df["Volume"].round(8)

    # Reset index to include Date and Time in the CSV
    df.reset_index(inplace=True)

    if csv:
        df.to_csv("data.csv", index=True)
        print("Data saved")

    return df


def load_csv(start_date=None, end_date=None):
    """Load historical data from a CSV file."""
    df = pd.read_csv("data.csv", index_col="Date", parse_dates=True)
    if start_date and end_date:
        return df.loc[start_date:end_date]

    return df


# fetch_historical_data("BTCUSDT", "2023-10-01", "2023-12-31", csv=True)


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


def calculate_trade_size(current_price):
    """Calculate the size of a trade for $20 based on the current price."""
    trade_size = 20 / current_price
    return trade_size
