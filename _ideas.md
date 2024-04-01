1. Stop loss on Arbitrage(BTC/ETH)
2. Sell after prices comes back(after bottom)
3. DCA if big profit
5. On 5% up or down -> buy signal
6. 1% profit sell(or 0.5%)
7. If major trend changes, positions are stale
8. Max trades are 7 based on api limits(can tweak)
9. Binance api -> 100/10s and 200,000/24h;
    -  We need to rotate API calls within a ~30 sec period to not hit rate limits
    -  We need 1 request to fetch data
    -  We need 1 or more requests to get price; buy; sell and more
    -  Amazon 1bil requests/month -> ~6$. Each week will be around 1mil requests