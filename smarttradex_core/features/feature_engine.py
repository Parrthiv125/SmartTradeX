# smarttradex_core/features/feature_engine.py

class FeatureEngine:
    def build_features(self, candles: list):
        if len(candles) < 2:
            return None

        prev_close = candles[-2]["close"]
        last_close = candles[-1]["close"]

        price_return = (last_close - prev_close) / prev_close

        return {
            "return": price_return
        }
