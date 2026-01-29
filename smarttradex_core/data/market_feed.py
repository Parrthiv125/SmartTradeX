# smarttradex_core/data/market_feed.py

from smarttradex_core.data.exchange_base import ExchangeBase


class MarketFeed:
    def __init__(self, exchange: ExchangeBase):
        self.exchange = exchange
        self.latest_candle = None

    def update(self):
        """
        Fetch latest candle from exchange and store it.
        """
        self.latest_candle = self.exchange.fetch_latest_candle()
        return self.latest_candle

    def get_latest(self):
        return self.latest_candle
