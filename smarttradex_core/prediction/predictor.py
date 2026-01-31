# smarttradex_core/prediction/predictor.py

class Predictor:
    def predict(self, features: dict):
        if not features:
            return 0.0

        return features["return"]
