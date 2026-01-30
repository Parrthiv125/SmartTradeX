from smarttradex_core.data.binance_client import BinanceClient
from smarttradex_core.data.market_feed import MarketFeed

client = BinanceClient()
feed = MarketFeed(client)

candle = feed.update()

assert "close" in candle
assert candle["close"] > 0

print("Binance REST feed test passed")
