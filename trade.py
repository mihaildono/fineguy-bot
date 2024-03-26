from binance.client import Client
from trend import check_trend
from client import binance_client

def get_dollar_quantity(symbol, amount_in_dollars):
    """Calculate the quantity needed for a trade of approximately $1."""
    avg_price = binance_client.get_avg_price(symbol=symbol)
    current_price = float(avg_price['price'])
    quantity = amount_in_dollars / current_price
    return quantity

def place_order(symbol, side, quantity):
    """Place an order on Binance."""
    try:
        order = binance_client.create_order(symbol=symbol,
                                    side=side,
                                    type=Client.ORDER_TYPE_MARKET,
                                    quantity=quantity)
        return order
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def trade_symbol(symbol, amount_in_dollars=1):
    trend = check_trend(symbol)

    if trend == "BULLISH":
        # Calculate quantity for a long (buy) order of approximately $1
        quantity = get_dollar_quantity(symbol, amount_in_dollars)
        # Place a long order
        order = place_order(symbol, Client.SIDE_BUY, quantity)
    elif trend == "BEARISH":
        # For educational purposes, this simulates a short by selling. In real trading, this would require borrowing.
        # Calculate quantity for a short (sell) order of approximately $1
        quantity = get_dollar_quantity(symbol, amount_in_dollars)
        # Place a short order, simplified, actual shorting is more complex
        order = place_order(symbol, Client.SIDE_SELL, quantity)

    if order is not None:
        print(f"Order placed: {order}")