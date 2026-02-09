# smarttradex_core/prediction/predictor.py

import joblib
import os
import numpy as np
import pandas as pd


class Predictor:
    """
    ML-first predictor with calibrated thresholds
    and expanded feature support.
    """

    # ─────────────────────────────────────────────
    # INIT
    # ─────────────────────────────────────────────
    def __init__(self):

        model_path = "models_store/btc_5m_model/model.pkl"

        self.model = None

        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            print("[PREDICTOR] ML model loaded")
        else:
            print("[PREDICTOR] No model found → fallback active")

        # Calibrated threshold (balanced mode)
        self.THRESHOLD = 0.0012

    # ─────────────────────────────────────────────
    # MAIN PREDICTION
    # ─────────────────────────────────────────────
    def predict(self, features: dict):

        if features is None:
            return {
                "action": "HOLD",
                "confidence": 0,
                "reason": "no_features"
            }

        # =========================================================
        # ML INFERENCE
        # =========================================================
        if self.model:

            feature_vector = pd.DataFrame([{
                "ret_1": features["ret_1"],
                "ret_5": features["ret_5"],
                "ret_15": features["ret_15"],
                "vol_5": features["vol_5"],
                "vol_15": features["vol_15"],
                "rsi": features["rsi"],
                "ema_fast": features["ema_fast"],
                "ema_slow": features["ema_slow"],
                "ema_spread": features["ema_spread"],
                "trend_slope": features["trend_slope"]
            }])

            pred_return = self.model.predict(
                feature_vector
            )[0]

            # ───────── SIGNAL MAPPING ─────────
            if pred_return > self.THRESHOLD:
                action = "BUY"

            elif pred_return < -self.THRESHOLD:
                action = "SELL"

            else:
                action = "HOLD"

            # Confidence scaling
            confidence = min(
                abs(pred_return) / self.THRESHOLD,
                1
            )

            prediction = {
                "action": action,
                "confidence": round(confidence, 4),
                "predicted_return": float(pred_return),
                "source": "ml_model"
            }

            print(
                f"[ML] Predicted={round(pred_return,6)} "
                f"→ {action} "
                f"(conf={prediction['confidence']})"
            )

            return prediction

        # =========================================================
        # RULE FALLBACK
        # =========================================================
        r1 = features["ret_1"]
        r5 = features["ret_5"]

        THRESHOLD_1M = 0.0005
        THRESHOLD_5M = 0.0010

        action = "HOLD"

        if r1 > THRESHOLD_1M and r5 > THRESHOLD_5M:
            action = "BUY"

        elif r1 < -THRESHOLD_1M and r5 < -THRESHOLD_5M:
            action = "SELL"

        confidence = abs(r1) + abs(r5)

        prediction = {
            "action": action,
            "confidence": round(confidence, 4),
            "reason": "rule_fallback"
        }

        print(
            f"[RULE] ret1={round(r1,5)} "
            f"ret5={round(r5,5)} → {action}"
        )

        return prediction
