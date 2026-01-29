# smarttradex_core/data/market_feed.py

class MarketFeed:
    def __init__(self):
        self.latest_candle = None

    def update(self, candle: dict):
        self.latest_candle = candle

    def get_latest(self):
        return self.latest_candle
