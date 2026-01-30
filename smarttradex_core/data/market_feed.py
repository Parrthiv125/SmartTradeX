import time


class MarketFeed:
    """
    Polls market data from exchange using REST.
    """

    def __init__(self, exchange, symbol="BTCUSDT", interval="1m"):
        self.exchange = exchange
        self.symbol = symbol
        self.interval = interval

    def update(self):
        time.sleep(1)  # SAFE rate limit
        return self.exchange.get_latest_candle(
            symbol=self.symbol,
            interval=self.interval
        )
