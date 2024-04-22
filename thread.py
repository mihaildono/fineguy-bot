from queue import Queue
import threading
import time
import websocket


def data_fetcher(coins, queue, interval):
    """Thread that periodically fetches data and ensures only the latest data is in the queue."""
    try:
        while True:
            data = fetch_intial_data(coins)
            with queue.mutex:  # Lock the queue to clear and insert atomically
                queue.queue.clear()
            queue.put(data)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Periodic data fetching stopped.")


def websocket_data_handler(ws, message):
    """WebSocket callback to handle incoming messages."""
    data = process_websocket_message(
        message
    )  # Assume this function parses and returns the data
    with data_queue.mutex:
        data_queue.queue.clear()
    data_queue.put(data)


def start_websocket_client(queue, url):
    """Starts a WebSocket client that connects to the given URL and handles incoming data."""
    ws = websocket.WebSocketApp(url, on_message=websocket_data_handler)
    ws.run_forever()


def main_bot_function(queue):
    """Main function that processes the latest data from the queue."""
    try:
        while True:
            data = queue.get()
            process_data(data)
            queue.task_done()
    except KeyboardInterrupt:
        print("Bot has been stopped manually.")


def process_data(data):
    # Process the data
    print("Processing data:", data)
    # Add your actual processing logic here


# Setting up the threads and queue
data_queue = Queue()
coins = "BTC"
interval = 60
websocket_url = "wss://example.com/websocket"  # URL to your WebSocket server

# Thread for fetching data periodically
fetch_thread = threading.Thread(target=data_fetcher, args=(coins, data_queue, interval))
fetch_thread.start()

# Thread for WebSocket connection
websocket_thread = threading.Thread(
    target=start_websocket_client, args=(data_queue, websocket_url)
)
websocket_thread.start()

# Main bot thread
bot_thread = threading.Thread(target=main_bot_function, args=(data_queue,))
bot_thread.start()
