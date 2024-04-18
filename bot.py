from binance_websocket import run_websocket
from api import fetch_intial_data


def run_bot():
    """Run the trading bot."""
    # Modify this list with coins of your choiec
    trading_coins = ["BTC", "ETH"]
    data = fetch_intial_data(trading_coins)
    run_websocket(data)


run_bot()
