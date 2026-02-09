import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import joblib


# ─────────────────────────────────────────────
# LOAD EXPANDED DATASET
# ─────────────────────────────────────────────
df = pd.read_csv(
    r"D:\SmartTradeX\btc_expanded_features.csv"
)

print("Expanded dataset shape:", df.shape)


# ─────────────────────────────────────────────
# FEATURES / TARGET
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
# TRAIN / TEST SPLIT
# ─────────────────────────────────────────────
split_index = int(len(df) * 0.8)

X_train = X[:split_index]
X_test = X[split_index:]

y_train = y[:split_index]
y_test = y[split_index:]


# ─────────────────────────────────────────────
# MODEL TRAINING
# ─────────────────────────────────────────────
model = GradientBoostingRegressor(
    n_estimators=220,
    learning_rate=0.05,
    max_depth=3
)

print("Training Gradient Boosting (expanded features)...")
model.fit(X_train, y_train)


# ─────────────────────────────────────────────
# EVALUATION
# ─────────────────────────────────────────────
preds = model.predict(X_test)

mse = mean_squared_error(y_test, preds)

print("MSE:", mse)


# ─────────────────────────────────────────────
# SAVE MODEL
# ─────────────────────────────────────────────
joblib.dump(
    model,
    "gb_expanded_model.pkl"
)

print("Model saved → gb_expanded_model.pkl")
