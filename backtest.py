from binance.client import Client
from trend import fetch_historical_data, check_trend


def open_position(position, entry_price, trade_amount, row):
    """Open a long or short position."""
    print(f"{position.capitalize()} entry at {entry_price}, Date: {row['open_time']}")
    quantity = trade_amount / entry_price
    return entry_price, quantity


def update_peak_profit(
    current_profit,
    peak_profit,
    trade_amount,
    profit_percentage,
    trailing_stop_activated,
):
    """Update peak profit and check for trailing stop activation."""
    if current_profit > peak_profit:
        peak_profit = current_profit
        if (
            peak_profit >= trade_amount * (profit_percentage / 100)
            and not trailing_stop_activated
        ):
            trailing_stop_activated = True
            print("Trailing stop activated")
    return peak_profit, trailing_stop_activated


def close_position(position, exit_price, current_profit, row):
    """Close the current position."""
    print(
        f"Exited {position} at {exit_price}, Profit: {current_profit}, Date: {row['open_time']}"
    )
    print("Exited due to trailing stop")
    print("---------------------------------")
    return current_profit


def calculate_current_profit(position, row, entry_price, quantity):
    """Calculate the current profit based on the position."""
    return (
        (row["close"] - entry_price) * quantity
        if position == "long"
        else (entry_price - row["close"]) * quantity
    )


def backtest_symbol(symbol, start_date, end_date):
    """Backtest a trading strategy for a symbol with simulated trailing stop logic."""
    df = fetch_historical_data(symbol, start_date, end_date)

    # Initial conditions
    trade_amount = 100
    profit_percentage = 0.5
    initial_balance = 10000
    balance = initial_balance
    position = None
    entry_price = 0
    quantity = 0
    peak_profit = 0
    trailing_stop_activated = False

    for index, row in df.iterrows():
        trend = check_trend(df, index)

        if trend == "BULLISH" and position is None:
            entry_price, quantity = open_position(
                "long", row["close"], trade_amount, row
            )
            position = "long"
            peak_profit = 0
            trailing_stop_activated = False

        if trend == "BEARISH" and position is None:
            entry_price, quantity = open_position(
                "short", row["close"], trade_amount, row
            )
            position = "short"
            peak_profit = 0
            trailing_stop_activated = False

        if position:
            current_profit = calculate_current_profit(
                position, row, entry_price, quantity
            )
            peak_profit, trailing_stop_activated = update_peak_profit(
                current_profit,
                peak_profit,
                trade_amount,
                profit_percentage,
                trailing_stop_activated,
            )

            if trailing_stop_activated and (peak_profit - current_profit) >= (
                trade_amount * (profit_percentage / 100)
            ):
                balance += close_position(position, row["close"], current_profit, row)
                position = None

    total_profit_loss = balance - initial_balance
    print()
    print(f"Backtest complete. Total Profit/Loss: {total_profit_loss}")
    return total_profit_loss
