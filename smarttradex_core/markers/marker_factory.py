# smarttradex_core/markers/marker_factory.py

class MarkerFactory:
    """
    Converts predictions into BUY / SELL / HOLD markers.
    """

    def __init__(self, threshold: float = 0.1):
        self.threshold = threshold

    def create_marker(self, prediction: dict) -> dict:
        if not prediction:
            return {}

        delta = prediction.get("predicted_delta_pct", 0.0)

        if delta > self.threshold:
            action = "BUY"
        elif delta < -self.threshold:
            action = "SELL"
        else:
            action = "HOLD"

        return {
            "action": action,
            "confidence": prediction.get("confidence", 0.0),
            "delta": delta
        }
