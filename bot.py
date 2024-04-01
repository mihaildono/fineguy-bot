import time
from trend import check_trend
from trade import trade_symbol
from backtest import backtest_symbol
from utils import get_top_20_symbols, get_df


# TODO: Limit trading to max 10 open orders, create a new func
def main():
    while True:
        top_20_symbols = get_top_20_symbols()
        for symbol in top_20_symbols:
            try:
                # Check the market trend for each symbol
                df = get_df(symbol)
                trend = check_trend(df)

                # Execute trade based on the trend
                trade_symbol(symbol, trend)

                # Delay before the next trade
                time.sleep(2)
            except Exception as e:
                print(f"An error occurred with {symbol}: {e}")

        # Wait before the next cycle of checking and trading
        print("Completed a cycle of trades. Waiting for the next cycle.")
        time.sleep(60 * 15)  # Example: 15 minutes


def main_backtest():
    # TODO: Add here list of bull/bear/sideways market dates and symbols
    # backtest("BTCUSDT", "2023-01-01", "2023-12-31")
    start_date = "2023-10-01"
    end_date = "2023-12-31"
    total_profit_loss = 0
    symbol = "BTCUSDT"
    # symbol = "ETHUSDT"
    try:
        # profit_loss = backtest_symbol(symbol, start_date, end_date)
        profit_loss = backtest_symbol(symbol, start_date, end_date)
        total_profit_loss += profit_loss
        print(f"Backtest result for {symbol}: Profit/Loss = {profit_loss}")
    except Exception as e:
        print(f"An error occurred with {symbol}: {e}")

    print(f"Total Profit/Loss for all symbols: {total_profit_loss}")


# Execute Program
if __name__ == "__main__":
    main_backtest()
