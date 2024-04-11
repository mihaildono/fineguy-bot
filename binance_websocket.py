import websocket
import json


# TODO: start listening for data and collecting data points
# Each socket is predefined
def on_message(ws, message):
    data = json.loads(message)
    print("Received data:")
    print(data)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")

    # Subscribe to the BTCUSDT ticker
    subscribe_message = {"method": "SUBSCRIBE", "params": ["btcusdt@ticker"], "id": 1}

    ws.send(json.dumps(subscribe_message))


def connect():
    websocket.enableTrace(True)
    binance_socket = "wss://stream.binance.com:9443/ws/btcusdt@miniTicker"
    ws = websocket.WebSocketApp(
        binance_socket, on_message=on_message, on_error=on_error, on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()


# Alternative
# from binance.client import Client
# from binance.websockets import BinanceSocketManager
# from twisted.internet import reactor


# def process_message(msg):
#     """Process live data and apply trading strategy."""
#     # This function will be called every time new data is received.
#     print("Message type:", msg["e"])
#     print(msg)
#     # Here, you'd insert your trading logic, deciding whether to buy or sell based on the incoming data.

#     bm = BinanceSocketManager(client)

#     # For this example, we're subscribing to live ticker data for BTCUSDT. Adjust as needed.
#     conn_key = bm.start_symbol_ticker_socket("BTCUSDT", process_message)

#     # Start the WebSocket
#     bm.start()
#     reactor.run()
