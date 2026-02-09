import pandas as pd
from sklearn.ensemble import RandomForestRegressor
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
# FEATURE / TARGET SPLIT
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
# TRAIN / TEST SPLIT (time series safe)
# ─────────────────────────────────────────────
split_index = int(len(df) * 0.8)

X_train = X[:split_index]
X_test = X[split_index:]

y_train = y[:split_index]
y_test = y[split_index:]


# ─────────────────────────────────────────────
# MODEL TRAINING
# ─────────────────────────────────────────────
model = RandomForestRegressor(
    n_estimators=120,
    max_depth=12,
    n_jobs=-1
)

print("Training Random Forest (expanded features)...")
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
    "rf_expanded_model.pkl"
)

print("Model saved → rf_expanded_model.pkl")
