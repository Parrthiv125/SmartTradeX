from smarttradex_core.strategies.base_strategy import BaseStrategy


class BreakoutStrategy(BaseStrategy):
    """
    Trades only strong breakout predictions.
    Best suited for volatile markets.
    """

    def __init__(self):
        self.name = "Breakout"

        # High confidence required
        self.breakout_confidence = 0.75

    def generate_signal(self, prediction: dict):

        action = prediction.get("action", "HOLD")
        confidence = prediction.get("confidence", 0.0)

        # Only trade strong signals
        if confidence < self.breakout_confidence:
            return {
                "action": "HOLD",
                "confidence": confidence,
                "strategy": self.name
            }

        if action == "BUY":
            return {
                "action": "BUY",
                "confidence": confidence,
                "strategy": self.name
            }

        elif action == "SELL":
            return {
                "action": "SELL",
                "confidence": confidence,
                "strategy": self.name
            }

        return {
            "action": "HOLD",
            "confidence": confidence,
            "strategy": self.name
        }
