# smarttradex_core/features/feature_engine.py

import numpy as np
import pandas as pd


class FeatureEngine:
    """
    Advanced ML feature builder.

    Generates:
    - Multi-horizon returns
    - Volatility
    - RSI
    - EMA trend signals
    - Trend slope
    """

    # ─────────────────────────────────────────────
    # RSI
    # ─────────────────────────────────────────────
    def calculate_rsi(self, closes, period=14):

        series = pd.Series(closes)

        delta = series.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        return rsi.iloc[-1]

    # ─────────────────────────────────────────────
    # EMA
    # ─────────────────────────────────────────────
    def calculate_ema(self, closes, span):

        return (
            pd.Series(closes)
            .ewm(span=span, adjust=False)
            .mean()
            .iloc[-1]
        )

    # ─────────────────────────────────────────────
    # TREND SLOPE
    # ─────────────────────────────────────────────
    def calculate_trend_slope(self, closes, window=10):

        y = np.array(closes[-window:])
        x = np.arange(window)

        slope = np.polyfit(x, y, 1)[0]

        return slope

    # ─────────────────────────────────────────────
    # BUILD FULL FEATURE VECTOR
    # ─────────────────────────────────────────────
    def build_features(self, candles):

        if len(candles) < 50:
            return None

        closes = [c["close"] for c in candles]

        # ───────── RETURNS ─────────
        ret_1 = (closes[-1] - closes[-2]) / closes[-2]

        ret_5 = (closes[-1] - closes[-6]) / closes[-6]

        ret_15 = (closes[-1] - closes[-16]) / closes[-16]

        # ───────── VOLATILITY ─────────
        vol_5 = np.std(closes[-5:])

        vol_15 = np.std(closes[-15:])

        # ───────── RSI ─────────
        rsi = self.calculate_rsi(closes)

        # ───────── EMA ─────────
        ema_fast = self.calculate_ema(closes, 9)
        ema_slow = self.calculate_ema(closes, 21)

        ema_spread = ema_fast - ema_slow

        # ───────── TREND ─────────
        trend_slope = self.calculate_trend_slope(closes)

        return {
            "ret_1": ret_1,
            "ret_5": ret_5,
            "ret_15": ret_15,
            "vol_5": vol_5,
            "vol_15": vol_15,
            "rsi": rsi,
            "ema_fast": ema_fast,
            "ema_slow": ema_slow,
            "ema_spread": ema_spread,
            "trend_slope": trend_slope
        }
