import datetime
from binance.streams import ThreadedWebsocketManager
import pandas as pd
from trend import SMA


# TODO: add a queue or callback to receive data
def process_message(msg, prices_df):
    """Closure that processes incoming WebSocket messages and updates the SMA calculation."""
    print(msg)
    if msg["e"] == "error":
        print(msg["m"])
    else:
        # TODO: extract this in a function
        # Extract full kline data from the message
        kline = msg["k"]
        close_time = kline["t"]
        open_price = float(kline["o"])
        high_price = float(kline["h"])
        low_price = float(kline["l"])
        close_price = float(kline["c"])
        volume = float(kline["v"])
        number_of_trades = kline["n"]
        taker_buy_base_asset_volume = float(kline["V"])
        taker_buy_quote_asset_volume = float(kline["Q"])

        # Create a new DataFrame row from the extracted data
        new_row = pd.DataFrame(
            {
                "Open": [open_price],
                "High": [high_price],
                "Low": [low_price],
                "Close": [close_price],
                "Volume": [volume],
                "Number of Trades": [number_of_trades],
                "Taker Buy Base Asset Volume": [taker_buy_base_asset_volume],
                "Taker Buy Quote Asset Volume": [taker_buy_quote_asset_volume],
            }
        )

        # Append to the historical DataFrame and ensure it does not exceed 1000 entries
        prices_df = pd.concat([prices_df, new_row], ignore_index=True)
        if len(prices_df) > 1000:
            prices_df = prices_df.iloc[-1000:]  # Keep only the latest 1000 entries

        sma_values = SMA(prices_df["Close"], 5)
        print(
            f"Latest SMA: {sma_values.iloc[-1]}, Latest Price: {close_price}, Time: {datetime.datetime.fromtimestamp(close_time/1000).strftime('%Y-%m-%d %H:%M:%S')}"
        )

        return prices_df


def run_websocket(initial_prices):
    twm = ThreadedWebsocketManager()
    twm.start()
    symbol = "BNBBTC"

    print("Starting WebSocket...")
    twm.start_kline_socket(
        callback=(lambda msg: process_message(msg, initial_prices)),
        symbol=symbol,
    )
    print("WebSocket started. Joining...")
    twm.join()
