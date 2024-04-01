import time
from trend import check_trend
from trade import trade_symbol
from backtest import backtest_symbol
from utils import get_top_20_symbols, get_df, get_backtest_data


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
    """Backtest a trading strategy for multiple symbols."""
    results = []
    backtest_data = get_backtest_data()
    try:
        for data in backtest_data:
            symbol = data["symbol"]
            start_date = data["start_date"]
            end_date = data["end_date"]
            trend = data["trend"]
            print("--------------------")
            print(
                f"Backtesting {symbol} from {start_date} to {end_date} with trend: {trend}"
            )
            print("--------------------")
            profit_loss = backtest_symbol(symbol, start_date, end_date)
            results.append(
                {
                    "symbol": symbol,
                    "start_date": start_date,
                    "end_date": end_date,
                    "trend": trend,
                    "profit_loss": profit_loss,
                }
            )
            print("\n" * 2)
    except Exception as e:
        print(f"An error occurred with {symbol}: {e}")

    # Log the consolidated backtest results
    total_profit_loss = sum(result["profit_loss"] for result in results)
    for result in results:
        print(
            f"Backtest result for {result['symbol']} ({result['start_date']} to {result['end_date']}); trend: {result['trend']}: Profit/Loss = {result['profit_loss']}"
        )

    print(f"Total Profit/Loss for all symbols: {total_profit_loss}")


# Execute Program
if __name__ == "__main__":
    main_backtest()
