from binance_websocket import run_websocket
from api import fetch_indicators_data


# TODO: Add live charting
def run_bot():
    """Run the trading bot."""
    # Modify this list with coins of your choice
    trading_coins = ["BNB"]
    initial_data = fetch_indicators_data(trading_coins, "1m", 100)
    run_websocket(trading_coins)


run_bot()
