# smarttradex_core/markers/marker_factory.py

class MarkerFactory:
    def create_marker(self, prediction: float):
        if prediction > 0.001:
            action = "BUY"
        elif prediction < -0.001:
            action = "SELL"
        else:
            action = "HOLD"

        return {
            "action": action,
            "confidence": min(abs(prediction) * 100, 1.0),
            "delta": prediction
        }
