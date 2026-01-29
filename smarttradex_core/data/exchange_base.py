# smarttradex_core/data/exchange_base.py

from abc import ABC, abstractmethod


class ExchangeBase(ABC):
    """
    Abstract base class for all exchanges.
    """

    @abstractmethod
    def fetch_latest_candle(self):
        pass

    @abstractmethod
    def fetch_historical_candles(self, limit: int):
        pass
