# smarttradex_core/state.py

class EngineState:
    def __init__(self):
        self.market_data = None
        self.prediction = None
        self.signal = None
        self.position = None
        self.markers = []

    def reset(self):
        self.__init__()
