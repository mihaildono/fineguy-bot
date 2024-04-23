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


def trading_strategy(prices_df, symbol):
    """Evaluates the trading strategy based on SMA and executes buy orders."""
    prices_df["SMA"] = (
        prices_df["Close"].rolling(window=9).mean()
    )  # Calculate 9-period SMA

    # Check for a crossover buy signal: current price above SMA, previous price below SMA
    if (
        len(prices_df) > 1
        and prices_df["Close"].iloc[-1] > prices_df["SMA"].iloc[-1]
        and prices_df["Close"].iloc[-2] < prices_df["SMA"].iloc[-2]
    ):
        print("Buy signal detected.")
        order_result = place_order(symbol, Client.SIDE_BUY, 10)
        if order_result:
            print(f"Buy order placed successfully: {order_result}")
        else:
            print("Failed to place buy order.")
    else:
        print("No buy signal.")
