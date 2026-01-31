class Predictor:
    """
    Simple rule-based predictor.
    ML-ready structure.
    """

    def predict(self, features_1m: dict, features_5m: dict | None = None):
        """
        Generate a prediction using 1m and optional 5m features.
        """

        # Default prediction
        prediction = {
            "action": "HOLD",
            "confidence": 0.0,
            "reason": "no_signal"
        }

        if not features_1m:
            return prediction

        # 1-minute return (existing logic)
        return_1m = features_1m.get("return_1m", 0)

        # 5-minute return (new logic)
        return_5m = 0
        if features_5m:
            return_5m = features_5m.get("return_5m", 0)

        # Very simple combined logic (BEGINNER SAFE)
        if return_1m > 0 and return_5m > 0:
            prediction.update({
                "action": "BUY",
                "confidence": 0.6,
                "reason": "1m_and_5m_up"
            })

        elif return_1m < 0 and return_5m < 0:
            prediction.update({
                "action": "SELL",
                "confidence": 0.6,
                "reason": "1m_and_5m_down"
            })

        return prediction
