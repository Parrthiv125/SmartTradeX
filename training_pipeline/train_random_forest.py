import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib


# ─────────────────────────────────────────────
# LOAD DATASET
# ─────────────────────────────────────────────
df = pd.read_csv(r"D:\SmartTradeX\clean_data.csv")

print("Dataset shape:", df.shape)


# ─────────────────────────────────────────────
# FEATURE / TARGET SPLIT
# ─────────────────────────────────────────────
features = [
    "ret_1",
    "ret_5",
    "ret_15",
    "vol_5",
    "vol_15"
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
    n_estimators=100,
    max_depth=10,
    n_jobs=-1
)

print("Training Random Forest...")
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
joblib.dump(model, "rf_model.pkl")

print("Model saved → rf_model.pkl")
