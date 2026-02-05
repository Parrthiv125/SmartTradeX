class Predictor:
    """
    RULE-BASED PREDICTOR WITH NOISE FILTER

    Prevents micro-fluctuation trades.
    """

    def predict(self, features_1m: dict, features_5m: dict | None = None):

        r1 = features_1m.get("return", 0)

        r5 = 0
        if features_5m:
            r5 = features_5m.get("return", 0)

        # ── Thresholds (noise filter) ──────────
        THRESHOLD_1M = 0.0005   # 0.05%
        THRESHOLD_5M = 0.0010   # 0.10%

        action = "HOLD"

        if r1 > THRESHOLD_1M and r5 > THRESHOLD_5M:
            action = "BUY"

        elif r1 < -THRESHOLD_1M and r5 < -THRESHOLD_5M:
            action = "SELL"

        confidence = abs(r1) + abs(r5)

        prediction = {
            "action": action,
            "confidence": round(confidence, 4),
            "reason": "threshold_dual_tf"
        }

        print(
            f"[PREDICTOR] 1m={round(r1,5)} "
            f"5m={round(r5,5)} → {action}"
        )

        return prediction
