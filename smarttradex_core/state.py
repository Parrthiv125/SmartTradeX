# smarttradex_core/state.py

class EngineState:
    """
    Holds the current state of the trading engine.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.market_data = None
        self.prediction = None
        self.markers = []
        self.trades = []

    def snapshot(self) -> dict:
        """
        Return a serializable snapshot of engine state.
        """
        return {
            "market_data": self.market_data,
            "prediction": self.prediction,
            "markers": self.markers,
            "trades": self.trades
        }
