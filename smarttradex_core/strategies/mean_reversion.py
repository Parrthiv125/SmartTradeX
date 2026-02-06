from smarttradex_core.strategies.base_strategy import BaseStrategy


class MeanReversionStrategy(BaseStrategy):
    """
    Trades against prediction direction in range markets.
    Assumes price will revert to mean.
    """

    def __init__(self):
        self.name = "MeanReversion"

        # Confidence window for reversal trades
        self.min_confidence = 0.40
        self.max_confidence = 0.65

    def generate_signal(self, prediction: dict):

        action = prediction.get("action", "HOLD")
        confidence = prediction.get("confidence", 0.0)

        # Only trade mid-confidence predictions
        if not (self.min_confidence <= confidence <= self.max_confidence):
            return {
                "action": "HOLD",
                "confidence": confidence,
                "strategy": self.name
            }

        # Reverse prediction
        if action == "BUY":
            return {
                "action": "SELL",
                "confidence": confidence,
                "strategy": self.name
            }

        elif action == "SELL":
            return {
                "action": "BUY",
                "confidence": confidence,
                "strategy": self.name
            }

        return {
            "action": "HOLD",
            "confidence": confidence,
            "strategy": self.name
        }
