import pandas as pd

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


from backtesting import Backtest, Strategy


def EMA(values, span):
    # Convert the numpy array to a pandas Series
    series = pd.Series(values)
    return (
        series.ewm(span=span, adjust=False).mean().bfill().values
    )  # Use bfill() to ensure no NaN values at the beginning


class TrailingStopStrategy(Strategy):
    trade_amount = 100  # Amount in dollars for each trade
    trailing_stop_loss = None
    entry_price = 0
    trailing_stop_pct = 5

    def init(self):
        # Example strategy using EMA crossover
        self.ema_short = self.I(lambda x: EMA(x, span=9), self.data.Close)
        self.ema_long = self.I(lambda x: EMA(x, span=21), self.data.Close)

    def next(self):
        if not self.position:
            # Check if the EMA9 is above EMA21
            if self.ema_short[-1] > self.ema_long[-1]:
                # Calculate the quantity for $100 trades, ensuring it's more than the minimum size
                quantity = self.trade_amount / self.data.Close[-1]
                self.buy(size=quantity)
                self.entry_price = self.data.Close[-1]
                # Set the initial trailing stop loss to 5% below the entry price
                self.trailing_stop_loss = self.entry_price * (
                    1 - self.trailing_stop_pct / 100
                )
        else:
            # Update the trailing stop loss to the maximum of the current trailing stop loss
            # or the current price minus the trailing stop percentage
            self.trailing_stop_loss = max(
                self.trailing_stop_loss,
                self.data.Close[-1] * (1 - self.trailing_stop_pct / 100),
            )
            # Check to close the position based on the trailing stop loss
            if self.data.Close[-1] < self.trailing_stop_loss:
                self.position.close()


# yahoo finance Sep 17, 2014 - Apr 02, 2024, Daily
df = pd.read_csv("data.csv", parse_dates=["Date"], index_col="Date")
start_date = "2015-01-01"
end_date = "2017-01-01"
filtered_df = df.loc[start_date:end_date]

bt = Backtest(filtered_df, TrailingStopStrategy, cash=10000, commission=0.002)
results = bt.run()
print(results)

# Visualize the trades within the selected period
bt.plot()
