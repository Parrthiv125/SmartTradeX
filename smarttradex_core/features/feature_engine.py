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
    
    def build_5m_features(self, candle_5m: dict):
        """
        Build basic features from a 5-minute candle.
        Returns empty dict if candle is None.
        """
        if candle_5m is None:
            return {}

        open_price = candle_5m["open"]
        close_price = candle_5m["close"]

        return {
            "return_5m": (close_price - open_price) / open_price
        }

