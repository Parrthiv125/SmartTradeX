class MarkerFactory:
<<<<<<< HEAD
    def create_marker(self, prediction):
        # prediction is now a dict, not a float
        value = prediction.get("value", 0.0)

        if value > 0.001:
            action = "BUY"
        elif value < -0.001:
            action = "SELL"
        else:
            action = "HOLD"
=======
    def create_marker(self, prediction: dict):
        """
        Convert predictor output into a marker.
        Beginner-safe: uses action string directly.
        """

        action = prediction.get("action", "HOLD")
>>>>>>> 71b5da3e728dd46887e7eeb2f7acca2c9f292e55

        return {
            "action": action,
            "confidence": prediction.get("confidence", 0.0),
<<<<<<< HEAD
            "delta": value
        }
=======
            "reason": prediction.get("reason", "unknown")
        }
>>>>>>> 71b5da3e728dd46887e7eeb2f7acca2c9f292e55
