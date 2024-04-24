import threading
import time
import pandas as pd
from trade import live_strategy_adapter
from api import fetch_historical_data

# Shared data structure with locking mechanism
data_lock = threading.Lock()
coin_data = (
    {}
)  # Dictionary to hold data for each coin: {'BTC': {'historical': DataFrame, 'realtime': DataFrame}, ...}


def update_data(coin, source, new_data):
    """Update the data for a specific coin and source."""
    with data_lock:
        if coin not in coin_data:
            coin_data[coin] = {"historical": pd.DataFrame(), "realtime": pd.DataFrame()}

        # Concatenate new data to the appropriate DataFrame, keeping only the latest data
        coin_data[coin][source] = pd.concat(
            [coin_data[coin][source], new_data], ignore_index=True
        )
        if len(coin_data[coin][source]) > 1000:  # Limit size to last 1000 entries
            coin_data[coin][source] = coin_data[coin][source].iloc[-1000:]


def get_latest_data(coin):
    """Safely fetch the latest data for a specific coin and source."""
    with data_lock:
        return coin_data.get(coin, {})


# NOTE: IMPROVEMENT: You can pass dict with indicators and timeframes
def poll_periodic_data(coins, interval, limit, fetch_interval):
    """Fetches historical data for a coin at regular intervals and updates the shared data structure."""
    while True:
        for coin in coins:
            print(f"Fetching historical data for {coin}...")
            historical_data = fetch_historical_data(coin, interval, limit)
            update_data(
                coin, "historical", historical_data
            )  # Assuming historical_data is structured correctly
        time.sleep(fetch_interval)


def analyze_data():
    """Analyzes data from the shared dictionary for trading decisions."""
    try:
        while True:
            for coin, sources in coin_data.items():
                # Skip if not populated yet
                if sources["historical"].empty or sources["realtime"].empty:
                    continue
                print(f"Analyzing data for {coin}...")
                latest_data = get_latest_data(coin)
                live_strategy_adapter(latest_data, coin)
            time.sleep(5)  # Check every 60 seconds
    except KeyboardInterrupt:
        print("Analysis stopped manually.")


def start_thread(coins):
    """Starts the threads for fetching periodical data and processing it."""
    print("Starting threads...")
    threading.Thread(
        target=poll_periodic_data, args=(coins, "4h", 1000, 60 * 60 * 4)
    ).start()

    print("Starting analysis thread...")
    analyze_thread = threading.Thread(target=analyze_data)
    analyze_thread.start()
