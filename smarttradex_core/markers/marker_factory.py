import time


class MarkerFactory:
    def create_marker(self, prediction: dict):
        """
        Convert predictor output into a marker.
        Engine-safe and GUI-safe.
        """

        action = prediction.get("action", "HOLD")

        return {
            "action": action,
            "confidence": prediction.get("confidence", 0.0),
            "reason": prediction.get("reason", "unknown"),

            # Required for chart plotting
            "timestamp": time.time(),
            "price": prediction.get("price")  # may be None
        }
