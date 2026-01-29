from smarttradex_core.data.exchange_base import ExchangeBase


class DummyExchange(ExchangeBase):
    def fetch_latest_candle(self):
        return {}

    def fetch_historical_candles(self, limit: int):
        return [{}] * limit


exchange = DummyExchange()

assert isinstance(exchange.fetch_latest_candle(), dict)
assert len(exchange.fetch_historical_candles(3)) == 3

print("ExchangeBase test passed")
