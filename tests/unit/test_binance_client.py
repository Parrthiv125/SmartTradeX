from smarttradex_core.data.binance_client import BinanceClient

client = BinanceClient()

latest = client.fetch_latest_candle()
assert latest["symbol"] == "BTCUSDT"
assert "close" in latest

history = client.fetch_historical_candles(limit=5)
assert len(history) == 5

print("BinanceClient skeleton test passed")
