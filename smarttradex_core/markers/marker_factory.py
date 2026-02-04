class MarkerFactory:
    def create_marker(self, prediction):
        # prediction is now a dict, not a float
        value = prediction.get("value", 0.0)

        if value > 0.001:
            action = "BUY"
        elif value < -0.001:
            action = "SELL"
        else:
            action = "HOLD"

        return {
            "action": action,
            "confidence": prediction.get("confidence", 0.0),
            "delta": value
        }