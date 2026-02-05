import time


class MarkerFactory:
    def create_marker(self, prediction: dict):
        """
        Convert predictor output into a marker.
        Beginner-safe: uses action string directly.
        """

        action = prediction.get("action", "HOLD")

        return {
            "action": action,
            "confidence": prediction.get("confidence", 0.0),
            "reason": prediction.get("reason", "unknown"),

            # ── Added for API / GUI compatibility ──
            "timestamp": time.time()
        }
