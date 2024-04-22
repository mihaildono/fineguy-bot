from utils import load_csv
from trend import EMA, PSAR
from plot import plot

from trend import get_trend
from utils import calculate_trade_size


import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


from backtesting import Backtest, Strategy


# TODO: Best to rewrite this as its buggy -> plot crashes and you cannot trade small fractions of a coin
class TradingStrategy(Strategy):
    def init(self):
        self.ema = self.I(EMA, self.data.Close, 200)
        self.psar = self.I(PSAR, self.data)
        self.in_position = False
        self.buy_price = None
        self.highest_close_since_buy = None  # Initialize for long positions
        self.lowest_close_since_sell = None  # Initialize for short positions
        self.stop_price = None
        self.initial_investment = 0

    def next(self):
        is_positive_trend, is_negative_trend = get_trend(
            self.data.Close[-1], self.ema[-1], self.psar[-1]
        )
        trade_size = round(calculate_trade_size(self.data.Close[-1]))
        # Entering a long position
        if not self.in_position and is_positive_trend:
            self.buy(size=trade_size)
            self.in_position = True
            self.buy_price = self.data.Close[-1]  #
            self.highest_close_since_buy = self.data.Close[-1]
            self.initial_investment = (
                self.buy_price * trade_size
            )  # For short, initial investment concept is the same
            self.stop_price = None

        # Entering a short position
        elif not self.in_position and is_negative_trend:
            self.sell(size=trade_size)
            self.in_position = True
            self.buy_price = self.data.Close[-1]
            self.lowest_close_since_sell = self.data.Close[-1]
            self.initial_investment = (
                self.buy_price * trade_size
            )  # For short, initial investment concept is the same
            self.stop_price = None

        # Check if it's time to exit a long position
        if self.in_position and self.highest_close_since_buy is not None:
            self.exit_long_position()

        # Check if it's time to exit a short position
        if self.in_position and self.lowest_close_since_sell is not None:
            self.exit_short_position()

    def exit_long_position(self):
        current_price = self.data.Close[-1]
        self.highest_close_since_buy = max(self.highest_close_since_buy, current_price)

        current_value = current_price * self.position.size
        profit_since_buy = (
            current_value - self.initial_investment
        ) / self.initial_investment

        # Update the stop price if profit has reached at least 2%
        if profit_since_buy >= 0.02:
            self.stop_price = self.highest_close_since_buy * 0.99

        # Exit the position based on the trailing stop
        if self.stop_price and current_price <= self.stop_price:
            self.position.close()
            self.reset_position()

    def exit_short_position(self):
        current_price = self.data.Close[-1]
        self.lowest_close_since_sell = min(self.lowest_close_since_sell, current_price)

        current_value = current_price * self.position.size
        profit_since_buy = (
            current_value - self.initial_investment
        ) / self.initial_investment

        # Update the stop price for the short position if there's a profit of more than 2%
        if profit_since_buy >= 0.02:
            self.stop_price = (
                self.lowest_close_since_sell * 1.01
            )  # Adjust for short position

        # Exit the position based on the trailing stop
        if self.stop_price and current_price >= self.stop_price:
            self.position.close()
            self.reset_position()

    def reset_position(self):
        """Resets variables to allow entering a new position."""
        self.in_position = False
        self.buy_price = None
        self.highest_close_since_buy = None
        self.lowest_close_since_sell = None
        self.stop_price = None
        self.initial_investment = 0  # Reset initial investment


df = load_csv()
bt = Backtest(
    df, TradingStrategy, cash=100000
)  # Can reduce cash if its a coin with less value
results = bt.run()
print(results)
# Visualize the trades within the selected period
bt.plot(resample=False)
plot(results, df)
