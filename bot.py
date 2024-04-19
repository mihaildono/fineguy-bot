from binance_websocket import run_websocket
from api import fetch_intial_data


def run_bot():
    """Run the trading bot."""
    # Modify this list with coins of your choice
    trading_coins = ["BNB"]
    initial_data = fetch_intial_data(trading_coins)
    run_websocket(initial_data["data"])


run_bot()
