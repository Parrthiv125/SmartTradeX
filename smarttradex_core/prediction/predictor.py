import random


class Predictor:
    """
    VALIDATION MODE — FORCED SIGNAL GENERATOR

    Purpose:
    Guarantee BUY / SELL signals so full trade pipeline
    can be validated end-to-end.
    """

    def predict(self, features_1m: dict, features_5m: dict | None = None):

        # Random forced signal
        action = random.choice(["BUY", "SELL"])

        prediction = {
            "action": action,
            "confidence": 0.5,
            "reason": "forced_validation_signal"
        }

        print(f"[PREDICTOR] Forced action: {action}")

        return prediction
