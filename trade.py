from binance.client import Client
from client import binance_client


def get_dollar_quantity(symbol, amount_in_dollars):
    """Calculate the quantity needed for a trade of approximately $1."""
    avg_price = binance_client.get_avg_price(symbol=symbol)
    current_price = float(avg_price["price"])
    quantity = amount_in_dollars / current_price
    return quantity


def place_order(symbol, side, quantity):
    """Place an order on Binance."""
    try:
        order = binance_client.create_order(
            symbol=symbol, side=side, type=Client.ORDER_TYPE_MARKET, quantity=quantity
        )
        return order
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
