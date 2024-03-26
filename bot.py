import time
from trend import check_trend
from trade import trade_symbol
from backtest import backtest_symbol
from client import binance_client


def get_top_20_symbols():
    """Get the top 20 symbols by 24h trading volume."""
    tickers = binance_client.get_ticker()
    # Sort the tickers by 24h volume in descending order and filter out non-USDT pairs for simplicity
    sorted_tickers = sorted(
        tickers, key=lambda x: float(x["quoteVolume"]), reverse=True
    )
    top_20_symbols = [
        ticker["symbol"] for ticker in sorted_tickers if "USDT" in ticker["symbol"]
    ][:20]
    return top_20_symbols


def main():
    while True:
        top_20_symbols = get_top_20_symbols()
        for symbol in top_20_symbols:
            try:
                # Check the market trend for each symbol
                trend = check_trend(symbol)

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
    # Add here list of bull/bear/sideways market dates
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    top_20_symbols = get_top_20_symbols()

    total_profit_loss = 0
    for symbol in top_20_symbols:
        try:
            profit_loss = backtest_symbol(symbol, start_date, end_date)
            total_profit_loss += profit_loss
            print(f"Backtest result for {symbol}: Profit/Loss = {profit_loss}")
        except Exception as e:
            print(f"An error occurred with {symbol}: {e}")

    print(f"Total Profit/Loss for all symbols: {total_profit_loss}")


# Execute Program
if __name__ == "__main__":
    main_backtest()
