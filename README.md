# FineGuy Bot
Trade crypto on binance.

# Prerequisites
1. Python3
2. Install requirements.txt
3. Add env vars. Change client api keys with your own(see _client.py) OR add env vars

NOTE: Change urls from testnet to production(if you want to use real money)(see websocket.py and api.py)

# How to run
- Execute bot.py
```sh
    python bot.py
```

# Trading Strategy
For now we assume that we are going to have two sets of data:
1. Real time data, we will calculate this data on the fly from websocket
2. Periodical long term data. This will be fetched on longer intervals,
   so we dont need to aggregate realtime data

# Project Structure
1. Bot.py
   - Main entry file for live and mock testing
2. Trend.py
   - Different trading indicators. You can import them to create your own trading strategy
3. Backtest.py
   - Run this file to test your strategy against custom or predefined period in the past
3. Thread.py
   - Manage threads and data from diffrent data sources