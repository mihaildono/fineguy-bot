from client import binance_client
import pandas as pd


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


def fetch_intial_data(coins):
    # fetch_balance(coins)
    # fetch_historical_data("BTC", "1h", 1000)
    historical_closing_prices = fetch_historical_data("BNB", "1m", 100)
    return historical_closing_prices
