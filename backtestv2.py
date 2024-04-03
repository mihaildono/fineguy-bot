import pandas as pd

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


from backtesting import Backtest, Strategy


def EMA(data, span):
    return pd.Series(data).ewm(span=span, adjust=False).mean().bfill()


class TrailingStopStrategy(Strategy):
    trade_amount = 100  # Amount in dollars for each trade
    entry_price = 0
    entry_date = None  # To keep track of the entry date
    last_high_price = 0  # Track the highest price since buying
    trailing_stop_pct = 1  # Stop loss to 1% loss
    profit_activation_pct = 2  # Activate trailing stop after 2% profit
    is_trailing_stop_activated = False  # Flag to track trailing stop activation

    def init(self):
        self.ema_short = self.I(lambda x: EMA(x, 9), self.data.Close)
        self.ema_long = self.I(lambda x: EMA(x, 21), self.data.Close)

    def next(self):
        price = self.data.Close[-1]
        date = self.data.index[-1]  # Get the current date
        quantity = self.trade_amount / price

        if not self.position and self.ema_short[-1] > self.ema_long[-1]:
            self.buy(size=quantity)
            self.entry_price = price
            self.entry_date = date  # Record entry date
            self.last_high_price = price  # Initialize last high price
            print(f"Bought at: {price} on {date}")
            return

        current_profit_pct = (price - self.entry_price) / self.entry_price * 100
        # Update the last high price if the current price is higher
        if price > self.last_high_price:
            self.last_high_price = price
            # Check if profit activation condition is met
            if current_profit_pct > self.profit_activation_pct:
                self.is_trailing_stop_activated = True
                self.trailing_stop_loss = self.last_high_price * (
                    1 - self.trailing_stop_pct / 100
                )
        # Check to close the position based on the trailing stop loss
        if self.is_trailing_stop_activated and price < self.trailing_stop_loss:
            self.position.close()
            profit = (price - self.entry_price) * quantity  # Calculate profit
            print(
                f"Sold at: {price} on {date}, Profit: {profit}, Profit%: {current_profit_pct}"
            )
            self.is_trailing_stop_activated = (
                False  # Reset flag after closing the position
            )


# yahoo finance Sep 17, 2014 - Apr 02, 2024, Daily BTC
df = pd.read_csv("data.csv", parse_dates=["Date"], index_col="Date")
start_date = "2015-01-01"
end_date = "2017-01-01"
filtered_df = df.loc[start_date:end_date]

bt = Backtest(filtered_df, TrailingStopStrategy, cash=10000, commission=0.002)
results = bt.run()
print(results)

# Visualize the trades within the selected period
bt.plot()
