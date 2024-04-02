import websocket
import json


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
