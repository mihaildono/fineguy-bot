from client import binance_client
import pandas as pd
from trend import EMA, SMA


def fetch_balance(coins):
    """Fetch the balance of the specified coins."""
    account_info = binance_client.get_account()

    # Create a dictionary to store balances of the specified coins
    specified_balances = {}

    # Check if each specified coin has a balance and add it to the dictionary
    for balance in account_info["balances"]:
        if balance["asset"] in coins:
            specified_balances[balance["asset"]] = balance["free"]

    return specified_balances


def fetch_historical_data(coin, interval, limit):
    symbol = f"{coin}USDT"
    klines = binance_client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(
        klines,
        columns=[
            "Open Time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "Close Time",
            "Quote Asset Volume",
            "Number of Trades",
            "Taker Buy Base Asset Volume",
            "Taker Buy Quote Asset Volume",
            "Ignore",
        ],
    )
    df["Close"] = pd.to_numeric(df["Close"])
    return df


# Add support for multiple coins
def fetch_intial_data(coins):
    """Get long term indicators. This function should be used to get the indicators that are not updated in real-time.
    If you want to get real-time indicators, use the websocket instead."""
    data = fetch_historical_data("BNB", "1m", 100)
    ema = EMA(data["Close"], 9)
    sma = SMA(data["Close"], 9)
    return {"ema": ema.iloc[-1], "sma": sma.iloc[-1], "data": data}
