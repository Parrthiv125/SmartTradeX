import pandas as pd
import numpy as np
import joblib


# ─────────────────────────────────────────────
# LOAD DATASET
# ─────────────────────────────────────────────
df = pd.read_csv(
    r"D:\SmartTradeX\btc_expanded_features.csv"
)

print("Dataset loaded:", df.shape)


# ─────────────────────────────────────────────
# FEATURES
# ─────────────────────────────────────────────
features = [
    "ret_1",
    "ret_5",
    "ret_15",
    "vol_5",
    "vol_15",
    "rsi",
    "ema_fast",
    "ema_slow",
    "ema_spread",
    "trend_slope"
]

X = df[features]
y = df["y"]


# ─────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────
model = joblib.load(
    "models_store/btc_5m_model/model.pkl"
)

print("Model loaded")


# ─────────────────────────────────────────────
# PREDICTIONS
# ─────────────────────────────────────────────
preds = model.predict(X)


# ─────────────────────────────────────────────
# THRESHOLD TESTING
# ─────────────────────────────────────────────
thresholds = np.arange(0.0002, 0.003, 0.0002)

results = []

for t in thresholds:

    trade_mask = abs(preds) > t

    trade_preds = preds[trade_mask]
    trade_actual = y[trade_mask]

    if len(trade_preds) == 0:
        continue

    pred_dir = np.sign(trade_preds)
    actual_dir = np.sign(trade_actual)

    accuracy = (pred_dir == actual_dir).sum() / len(trade_preds)

    results.append((t, accuracy, len(trade_preds)))


# ─────────────────────────────────────────────
# DISPLAY RESULTS
# ─────────────────────────────────────────────
print("\n=== THRESHOLD CALIBRATION ===")

for t, acc, count in results:

    print(
        f"Threshold: {t:.4f} | "
        f"Accuracy: {acc:.4f} | "
        f"Signals: {count}"
    )


# ─────────────────────────────────────────────
# BEST THRESHOLD
# ─────────────────────────────────────────────
best = max(results, key=lambda x: x[1])

print("\n=== BEST THRESHOLD ===")
print(
    f"Threshold: {best[0]:.4f} | "
    f"Accuracy: {best[1]:.4f} | "
    f"Signals: {best[2]}"
)
