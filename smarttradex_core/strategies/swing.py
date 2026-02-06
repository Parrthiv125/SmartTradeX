from smarttradex_core.strategies.base_strategy import BaseStrategy


class SwingStrategy(BaseStrategy):
    """
    Balanced strategy for mixed market conditions.
    Acts as fallback when regime is unclear.
    """

    def __init__(self):
        self.name = "Swing"

        # Moderate confidence window
        self.min_confidence = 0.55
        self.max_confidence = 0.75

    def generate_signal(self, prediction: dict):

        action = prediction.get("action", "HOLD")
        confidence = prediction.get("confidence", 0.0)

        # Only trade moderate confidence
        if not (self.min_confidence <= confidence <= self.max_confidence):
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
