import pandas as pd
from client import binance_client
from trend import get_trend_indicators


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
    klines = binance_client.get_klines(symbol=coin, interval=interval, limit=limit)
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


def fetch_indicators_data(coins, interval, limit):
    """Get long term indicators. This function should be used to get the indicators that are not updated in real-time.
    If you want to get real-time indicators, use the websocket instead."""
    data = {}
    for coin in coins:
        df = fetch_historical_data(coin, interval, limit)
        indicators = get_trend_indicators(df["Close"])
        data.update({coin: {**indicators, "data": df}})

    return data
