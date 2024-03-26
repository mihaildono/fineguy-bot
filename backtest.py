from binance.client import Client
from trend import fetch_historical_data, check_trend_for_date


def backtest_symbol(symbol, start_date, end_date):
    df = fetch_historical_data(symbol, Client.KLINE_INTERVAL_1DAY, start_date, end_date)

    # Initial conditions
    initial_balance = 10000  # Starting with a balance, for example, $10,000
    balance = initial_balance
    position_open = False
    entry_price = 0

    # Simulate trading
    for index, row in df.iterrows():
        trend = check_trend_for_date(df, index)

        if trend == "BULLISH" and not position_open:
            # Go long
            position_open = True
            entry_price = row["close"]
            print(f"Bought at {entry_price}")

        elif trend == "BEARISH" and position_open:
            # Close long position
            position_open = False
            exit_price = row["close"]
            profit = exit_price - entry_price
            balance += profit
            print(f"Sold at {exit_price}, Profit: {profit}")

    # Close any open position at the end of the backtest period
    if position_open:
        exit_price = df.iloc[-1]["close"]
        profit = exit_price - entry_price
        balance += profit
        print(f"Sold at {exit_price}, Profit: {profit}")

    # Results
    total_profit_loss = balance - initial_balance
    print(f"Backtest complete. Total Profit/Loss: {total_profit_loss}")
    return total_profit_loss


# Example usage
# backtest("BTCUSDT", "2023-01-01", "2023-12-31")
