from binance.streams import ThreadedWebsocketManager
import pandas as pd
from trend import get_trend_indicators


def extract_data_from_message(msg):
    """Extracts kline data from the message and creates a DataFrame row."""
    kline = msg["k"]
    return pd.DataFrame(
        {
            "Open": [float(kline["o"])],
            "High": [float(kline["h"])],
            "Low": [float(kline["l"])],
            "Close": [float(kline["c"])],
            "Volume": [float(kline["v"])],
            "Number of Trades": [kline["n"]],
            "Taker Buy Base Asset Volume": [float(kline["V"])],
            "Taker Buy Quote Asset Volume": [float(kline["Q"])],
        }
    )


def process_message(msg):
    """Process incoming WebSocket messages."""
    # Kline is not closed and we exit
    if msg["data"]["k"]["x"] is False:
        return
    if msg["data"]["e"] == "error":
        print(msg["data"]["m"])
    else:
        # Create a new DataFrame row from the extracted data
        new_row = extract_data_from_message(msg["data"])

        # Append to the historical DataFrame and ensure it does not exceed 1000 entries
        # TODO: Get current dataframe from queue
        prices_df = pd.DataFrame()
        prices_df = pd.concat([prices_df, new_row], ignore_index=True)
        if len(prices_df) > 1000:
            prices_df = prices_df.iloc[-1000:]  # Keep only the latest 1000 entries

        indicators = get_trend_indicators(prices_df["Close"])
        print(f"Stream: {msg["stream"]}, SMA: {indicators['sma']}, Latest Price: {new_row['Close'].iloc[0]}")

        return prices_df


def run_websocket(coins):
    """Opens WebSocket for the specified coins. This will track the specified coins in real-time.
    It will also calculate indicators in real time. If you are doing scalp or high frequency trading,
    use this to calculate specific indicators in real-time. Otherwise poll using the api calls."""
    twm = ThreadedWebsocketManager()
    print("Starting WebSocket...")
    twm.start()
    streams = [f"{coin.lower()}@kline_1s" for coin in coins]
    twm.start_multiplex_socket(process_message, streams)
    print("WebSocket started. Joining...")
    twm.join()

run_websocket(["BNBUSDT", "BTCUSDT"])
