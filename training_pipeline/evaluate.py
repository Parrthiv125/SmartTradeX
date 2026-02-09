# training_pipeline/evaluate.py

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
# EXPANDED FEATURES
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
    "models_store/btc_5m_model/xgb_model.pkl"
)

print("Model loaded successfully")


# ─────────────────────────────────────────────
# GENERATE PREDICTIONS
# ─────────────────────────────────────────────
preds = model.predict(X)


# ─────────────────────────────────────────────
# RAW DIRECTION ACCURACY
# ─────────────────────────────────────────────
pred_dir = np.sign(preds)
actual_dir = np.sign(y)

correct = (pred_dir == actual_dir).sum()
accuracy = correct / len(y)

print("\n=== DIRECTION METRICS ===")
print(f"Direction Accuracy: {accuracy:.4f}")


# ─────────────────────────────────────────────
# TRADE SIGNAL ACCURACY
# ─────────────────────────────────────────────
threshold = 0.0005

trade_mask = abs(preds) > threshold

trade_preds = preds[trade_mask]
trade_actual = y[trade_mask]

trade_pred_dir = np.sign(trade_preds)
trade_actual_dir = np.sign(trade_actual)

trade_correct = (
    trade_pred_dir == trade_actual_dir
).sum()

trade_accuracy = (
    trade_correct / len(trade_preds)
)

print("\n=== TRADE SIGNAL METRICS ===")
print(f"Trade Signal Accuracy: {trade_accuracy:.4f}")
print(f"Total Trade Signals: {len(trade_preds)}")


# ─────────────────────────────────────────────
# BUY / SELL SPLIT
# ─────────────────────────────────────────────
buy_signals = (trade_preds > 0).sum()
sell_signals = (trade_preds < 0).sum()

print("\n=== SIGNAL DISTRIBUTION ===")
print(f"BUY signals: {buy_signals}")
print(f"SELL signals: {sell_signals}")
