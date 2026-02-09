import requests
import time


class BinanceClient:
    """
    Simple REST client for Binance.
    Beginner-safe: no websocket, no async.
    """

    BASE_URL = "https://api.binance.com"

    # ------------------------------------------------
    # Fetch multiple candles (for scrolling charts)
    # ------------------------------------------------
    def get_candles(self, symbol="BTCUSDT", interval="1m", limit=200):
        """
        Fetch historical OHLCV candles.

        limit controls how many candles are returned.
        Larger limit → smoother scrolling chart.
        """

        url = f"{self.BASE_URL}/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
        }

        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        candles = []

        for c in data:
            candles.append({
                "time": int(c[0]),
                "open": float(c[1]),
                "high": float(c[2]),
                "low": float(c[3]),
                "close": float(c[4]),
                "volume": float(c[5]),
            })

        return candles

    # ------------------------------------------------
    # Keep single-candle method if needed elsewhere
    # ------------------------------------------------
    def get_latest_candle(self, symbol="BTCUSDT", interval="1m"):
        candles = self.get_candles(symbol, interval, limit=1)
        return candles[0]
