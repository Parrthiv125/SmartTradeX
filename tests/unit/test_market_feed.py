from smarttradex_core.data.market_feed import MarketFeed

feed = MarketFeed()

assert feed.get_latest() is None

sample = {"open": 1, "close": 2}
feed.update(sample)

assert feed.get_latest() == sample

print("MarketFeed test passed")
