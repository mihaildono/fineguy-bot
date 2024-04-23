from binance_websocket import run_websocket
from thread import start_thread


# TODO: Add live charting
def run_bot():
    """Run the trading bot."""
    # Modify this list with coins of your choice
    coins = ["BTCUSDT", "ETHUSDT"]
    start_thread(coins)
    run_websocket(coins)  # must be run second, or it blocks code


if __name__ == "__main__":
    run_bot()
