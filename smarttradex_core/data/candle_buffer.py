# smarttradex_core/data/candle_buffer.py

class CandleBuffer:
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.buffer = []

    def add_candle(self, candle: dict):
        self.buffer.append(candle)

        # keep buffer size bounded
        if len(self.buffer) > self.max_size:
            self.buffer.pop(0)

    def get_all(self):
        return self.buffer

    def get_last(self, n: int):
        """
        Return last n candles safely.
        """
        if n <= 0:
            return []
        return self.buffer[-n:]

    def clear(self):
        self.buffer = []
