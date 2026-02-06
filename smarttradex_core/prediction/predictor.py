import joblib
import os
import numpy as np
import pandas as pd


class Predictor:
    """
    AI + Rule Hybrid Predictor

    Uses ML model for prediction.
    Falls back to rule logic if model unavailable.
    """

    def __init__(self):

        model_path = "models_store/btc_5m_model/model.pkl"

        self.model = None

        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            print("[PREDICTOR] ML model loaded")
        else:
            print("[PREDICTOR] No model found → using rules")

    # ─────────────────────────────────────────────
    # MAIN PREDICTION
    # ─────────────────────────────────────────────
    def predict(self, features_1m: dict, features_5m: dict | None = None):

        r1 = features_1m.get("return", 0)
        r5 = 0

        if features_5m:
            r5 = features_5m.get("return", 0)

        # =========================================================
        # ML PREDICTION PATH
        # =========================================================
        if self.model:

            feature_vector = pd.DataFrame([{
                "ret_1": r1,
                "ret_5": r5,
                "ret_15": 0,
                "vol_5": abs(r1),
                "vol_15": abs(r5)
            }])

            pred_return = self.model.predict(feature_vector)[0]

            # Convert return → signal
            if pred_return > 0.0005:
                action = "BUY"
            elif pred_return < -0.0005:
                action = "SELL"
            else:
                action = "HOLD"

            confidence = min(abs(pred_return) * 1000, 1)

            prediction = {
                "action": action,
                "confidence": round(confidence, 4),
                "predicted_return": float(pred_return),
                "source": "ml_model"
            }

            print(
                f"[ML] Predicted return={round(pred_return,6)} "
                f"→ {action}"
            )

            return prediction

        # =========================================================
        # RULE FALLBACK
        # =========================================================
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
            f"[RULE] 1m={round(r1,5)} "
            f"5m={round(r5,5)} → {action}"
        )
        print("PREDICTION OUTPUT →", prediction)

        return prediction

