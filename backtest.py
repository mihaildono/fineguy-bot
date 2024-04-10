import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


from backtesting import Backtest, Strategy

from utils import load_csv
from trend import EMA, PSAR
from plot import plot


class TradingStrategy(Strategy):
    def init(self):
        self.ema = self.I(EMA, self.data.Close, 200)
        self.psar = self.I(PSAR, self.data)
        self.in_position = False
        self.buy_price = None
        self.highest_close_since_buy = 0
        self.stop_price = None  # Initialize stop price

    def next(self):
        is_over_psar = self.psar[-1] > self.data.Close[-1]
        is_under_ema = self.ema[-1] < self.data.Close[-1]
        if not self.in_position and is_over_psar and is_under_ema:
            self.buy()
            self.in_position = True
            self.buy_price = self.data.Close[-1]  # Store the buy price
            self.highest_close_since_buy = self.data.Close[
                -1
            ]  # Initialize with the current close price
            self.stop_price = None  # Reset stop price

        if self.in_position:
            current_price = self.data.Close[-1]
            self.highest_close_since_buy = max(
                self.highest_close_since_buy, current_price
            )

            if self.buy_price:  # Ensure buy_price is not None
                profit_since_buy = (
                    current_price / self.buy_price
                ) - 1  # Current profit since the buy

                # If profit has reached at least 2%, update the stop price
                if profit_since_buy >= 0.02:
                    # Update the stop price to be 1% below the highest close since buying
                    self.stop_price = self.highest_close_since_buy * 0.99

                # If a stop price has been set and the current price is below the stop price, sell
                if self.stop_price and current_price <= self.stop_price:
                    self.position.close()
                    self.in_position = False  # Reset position flag
                    self.buy_price = None  # Reset buy price
                    self.stop_price = None  # Reset stop price


df = load_csv()
bt = Backtest(
    df,
    TradingStrategy,
    cash=100000,
    commission=0.001,
)
results = bt.run()
print(results)
# Visualize the trades within the selected period
bt.plot(resample=False)
plot(results, df)
