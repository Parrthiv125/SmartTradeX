from smarttradex_core.data.market_feed import MarketFeed
from smarttradex_core.data.binance_client import BinanceClient

exchange = BinanceClient()
feed = MarketFeed(exchange)

assert feed.get_latest() is None

candle = feed.update()
assert candle is not None
assert feed.get_latest() == candle

print("MarketFeed exchange integration test passed")
