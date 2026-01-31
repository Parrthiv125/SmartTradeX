class CandleBuffer:
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.buffer = []

    def add_candle(self, candle: dict):
        """
        Add a single 1-minute candle to the buffer.
        """
        self.buffer.append(candle)

        # keep buffer size bounded
        if len(self.buffer) > self.max_size:
            self.buffer.pop(0)

    def get_all(self):
        """
        Return all stored candles.
        """
        return self.buffer

    def get_last(self, n: int):
        """
        Return last n candles safely.
        """
        if n <= 0:
            return []
        return self.buffer[-n:]

    def clear(self):
        """
        Clear the candle buffer.
        """
        self.buffer = []

    def get_last_5m_candle(self):
        """
        Aggregate last 5 one-minute candles into one 5-minute candle.
        Returns None if not enough data.
        """

        if len(self.buffer) < 5:
            return None

        last_five = self.buffer[-5:]

        open_price = last_five[0]["open"]
        close_price = last_five[-1]["close"]
        high_price = max(c["high"] for c in last_five)
        low_price = min(c["low"] for c in last_five)
        volume = sum(c["volume"] for c in last_five)
        timestamp = last_five[-1]["timestamp"]

        return {
            "timestamp": timestamp,
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "volume": volume,
        }
