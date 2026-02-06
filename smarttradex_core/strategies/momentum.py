from smarttradex_core.strategies.base_strategy import BaseStrategy


class MomentumStrategy(BaseStrategy):
    """
    Trades in direction of prediction momentum.
    Best suited for trending markets.
    """

    def __init__(self):
        self.name = "Momentum"

        # Confidence threshold for momentum trades
        self.min_confidence = 0.60

    def generate_signal(self, prediction: dict):

        action = prediction.get("action", "HOLD")
        confidence = prediction.get("confidence", 0.0)

        # Weak confidence → HOLD
        if confidence < self.min_confidence:
            return {
                "action": "HOLD",
                "confidence": confidence,
                "strategy": self.name
            }

        # Strong momentum trade
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
