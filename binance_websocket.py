from binance.streams import ThreadedWebsocketManager
import pandas as pd
from thread import update_data


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
        print(f"Processing message for {msg['stream']}...")
        coin = msg["stream"].split("@")[0].upper()  # Extract coin from the stream name
        new_row = extract_data_from_message(msg["data"])
        update_data(coin, "realtime", new_row)


def run_websocket(coins):
    """Opens WebSocket for the specified coins. This will track the specified coins in real-time.
    It will also calculate indicators in real time. If you are doing scalp or high frequency trading,
    use this to calculate specific indicators in real-time. Otherwise poll using the api calls.
    """
    twm = ThreadedWebsocketManager()
    print("Starting WebSocket...")
    twm.start()
    streams = [f"{coin.lower()}@kline_1s" for coin in coins]
    twm.start_multiplex_socket(process_message, streams)
    print("WebSocket started. Joining...")
    twm.join()
