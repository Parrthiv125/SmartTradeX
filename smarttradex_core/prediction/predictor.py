# smarttradex_core/prediction/predictor.py

class Predictor:
    """
    Model-agnostic prediction wrapper.
    """

    def __init__(self):
        pass

    def predict(self, features: dict) -> dict:
        """
        Return a dummy prediction.
        """
        if not features:
            return {}

        return {
            "predicted_delta_pct": 0.0,
            "confidence": 0.5,
            "direction": "HOLD"
        }
