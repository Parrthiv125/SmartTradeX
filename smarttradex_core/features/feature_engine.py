# smarttradex_core/features/feature_engine.py

import numpy as np


class FeatureEngine:
    """
    Builds ML-ready feature vectors from candle buffers.

    Supports:
    - 1m returns
    - Multi-horizon returns
    - Rolling volatility
    """

    # ─────────────────────────────────────────────
    # BUILD FULL FEATURE VECTOR
    # ─────────────────────────────────────────────
    def build_features(self, candles: list):
        """
        Expects list of candle dicts with 'close'.
        Requires at least 20 candles.
        """

        if len(candles) < 20:
            return None

        closes = [c["close"] for c in candles]

        # ───────── RETURNS ─────────
        ret_1 = (closes[-1] - closes[-2]) / closes[-2]

        ret_5 = (closes[-1] - closes[-6]) / closes[-6]

        ret_15 = (closes[-1] - closes[-16]) / closes[-16]

        # ───────── VOLATILITY ─────────
        vol_5 = np.std(closes[-5:])

        vol_15 = np.std(closes[-15:])

        return {
            "ret_1": ret_1,
            "ret_5": ret_5,
            "ret_15": ret_15,
            "vol_5": vol_5,
            "vol_15": vol_15
        }

    # ─────────────────────────────────────────────
    # LEGACY 1M FEATURE (for compatibility)
    # ─────────────────────────────────────────────
    def build_1m_legacy(self, candles: list):
        """
        Old system compatibility.
        """

        if len(candles) < 2:
            return None

        prev_close = candles[-2]["close"]
        last_close = candles[-1]["close"]

        price_return = (
            last_close - prev_close
        ) / prev_close

        return {
            "return": price_return
        }

    # ─────────────────────────────────────────────
    # LEGACY 5M FEATURE
    # ─────────────────────────────────────────────
    def build_5m_legacy(self, candle_5m: dict):
        """
        Old compatibility path.
        """

        if candle_5m is None:
            return {}

        open_price = candle_5m["open"]
        close_price = candle_5m["close"]

        return {
            "return_5m": (
                close_price - open_price
            ) / open_price
        }
