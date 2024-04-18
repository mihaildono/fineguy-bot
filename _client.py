from binance.client import Client

# Remove _ from the beginning of the file name and replace key and secret with your own

# Add environment variables for the API key and secret
api_key = "___YOUR_API_KEY___"
api_secret = "___YOUR_API_KEY___"

binance_client = Client(api_key, api_secret)

# comment this line if you want to use real money
binance_client.API_URL = "https://testnet.binance.vision/api"
