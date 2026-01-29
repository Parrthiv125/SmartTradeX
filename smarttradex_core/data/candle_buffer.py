# smarttradex_core/data/candle_buffer.py

class CandleBuffer:
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.buffer = []

    def add_candle(self, candle: dict):
        self.buffer.append(candle)
        if len(self.buffer) > self.max_size:
            self.buffer.pop(0)

    def get_all(self):
        return self.buffer

    def clear(self):
        self.buffer = []
