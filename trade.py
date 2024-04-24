from binance.client import Client
from client import binance_client
from trend import get_trend_indicators


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


def live_strategy_adapter(data, coin):
    """Adapter function to convert the data structure for the live trading strategy."""
    realtime_data = data["realtime"]
    historical_data = data["historical"]
    trading_strategy(realtime_data, historical_data, coin)


# TODO: Add live charting
def trading_strategy(realtime_df, historical_df, symbol):
    """Evaluates the trading strategy based on SMA and executes buy orders."""
    historical_indicators = get_trend_indicators(historical_df)
    realtime_indicators = get_trend_indicators(realtime_df)
    realtime_indicators["sma"] = (
        realtime_df["Close"].rolling(window=9).mean()
    )  # Calculate 9-period SMA

    # TODO: Add proper strategy for long/short
    if realtime_df["Close"].iloc[-1] > realtime_indicators["sma"].iloc[-1]:
        print("Buy signal detected.")
        order_result = place_order(symbol, Client.SIDE_BUY, 10)
        if order_result:
            print(f"Buy order placed successfully: {order_result}")
        else:
            print("Failed to place buy order.")
    else:
        print("No buy signal.")
