import requests
import time


class BinanceClient:
    """
    Simple REST client for Binance.
    Beginner-safe: no websocket, no async.
    """

    BASE_URL = "https://api.binance.com"

    def get_latest_candle(self, symbol="BTCUSDT", interval="1m"):
        url = f"{self.BASE_URL}/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": 1
        }

        response = requests.get(url, params=params, timeout=5)
        data = response.json()[0]

        return {
            "open": float(data[1]),
            "high": float(data[2]),
            "low": float(data[3]),
            "close": float(data[4]),
            "volume": float(data[5]),
            "timestamp": int(data[0])
        }
