from binance.client import Client
from trend import fetch_historical_data, check_trend


def backtest_symbol(symbol, start_date, end_date):
    """Backtest a trading strategy for a symbol with simulated trailing stop logic"""
    df = fetch_historical_data(symbol, start_date, end_date)

    # Initial conditions
    trade_amount = 100
    # profit_percentage = 1.0
    profit_percentage = 0.5
    initial_balance = 10000  # Starting with a balance, for example, $10,000
    balance = initial_balance
    position = None
    entry_price = 0
    quantity = 0  # Quantity bought, adjusted each trade to ensure specific trade amount position
    peak_profit = 0
    trailing_stop_activated = False

    for index, row in df.iterrows():
        trend = check_trend(df, index)

        if trend == "BULLISH" and position is None:
            # Open long position
            position = "long"
            entry_price = row["close"]
            quantity = trade_amount / entry_price
            peak_profit = 0
            trailing_stop_activated = False
            print(f"Long entry at {entry_price}, Date: {row['open_time']}")

        elif trend == "BEARISH" and position is None:
            # Open short position
            position = "short"
            entry_price = row["close"]
            quantity = trade_amount / entry_price
            peak_profit = 0
            trailing_stop_activated = False
            print(f"Short entry at {entry_price}, Date: {row['open_time']}")

        # Update trailing stop logic for both long and short positions
        if position:
            current_profit = (
                (row["close"] - entry_price) * quantity
                if position == "long"
                else (entry_price - row["close"]) * quantity
            )
            if current_profit > peak_profit:
                peak_profit = current_profit
                if (
                    peak_profit >= trade_amount * (profit_percentage / 100)
                    and not trailing_stop_activated
                ):
                    trailing_stop_activated = True
                    print("Trailing stop activated")

            if trailing_stop_activated and (peak_profit - current_profit) >= (
                trade_amount * (profit_percentage / 100)
            ):
                # Close position
                exit_price = row["close"]
                final_profit = current_profit
                balance += final_profit
                print(
                    f"Exited {position} at {exit_price}, Profit: {final_profit}, Date: {row['open_time']}"
                )
                print("Exited due to trailing stop")
                position = None
                print("---------------------------------")

    # Final results
    total_profit_loss = balance - initial_balance
    print(f"Backtest complete. Total Profit/Loss: {total_profit_loss}")
    return total_profit_loss
