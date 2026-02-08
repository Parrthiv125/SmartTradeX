import pandas as pd
import numpy as np


# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
df = pd.read_csv(r"D:\SmartTradeX\clean_data.csv")

print("Raw dataset:", df.shape)


# ─────────────────────────────────────────────
# RETURNS
# ─────────────────────────────────────────────
df["ret_1"] = df["close"].pct_change(1)

df["ret_5"] = df["close"].pct_change(5)

df["ret_15"] = df["close"].pct_change(15)


# ─────────────────────────────────────────────
# VOLATILITY
# ─────────────────────────────────────────────
df["vol_5"] = (
    df["close"]
    .rolling(5)
    .std()
)

df["vol_15"] = (
    df["close"]
    .rolling(15)
    .std()
)


# ─────────────────────────────────────────────
# RSI
# ─────────────────────────────────────────────
delta = df["close"].diff()

gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss

df["rsi"] = 100 - (100 / (1 + rs))


# ─────────────────────────────────────────────
# EMA
# ─────────────────────────────────────────────
df["ema_fast"] = (
    df["close"]
    .ewm(span=9, adjust=False)
    .mean()
)

df["ema_slow"] = (
    df["close"]
    .ewm(span=21, adjust=False)
    .mean()
)

df["ema_spread"] = (
    df["ema_fast"] - df["ema_slow"]
)


# ─────────────────────────────────────────────
# TREND SLOPE
# ─────────────────────────────────────────────
window = 10

slopes = []

for i in range(len(df)):

    if i < window:
        slopes.append(np.nan)
        continue

    y = df["close"].iloc[i-window:i].values
    x = np.arange(window)

    slope = np.polyfit(x, y, 1)[0]

    slopes.append(slope)

df["trend_slope"] = slopes


# ─────────────────────────────────────────────
# TARGET
# ─────────────────────────────────────────────
df["y"] = (
    df["close"]
    .shift(-5)
    .sub(df["close"])
    .div(df["close"])
)


# ─────────────────────────────────────────────
# CLEAN DATA
# ─────────────────────────────────────────────
df = df.dropna()

print("After feature build:", df.shape)


# ─────────────────────────────────────────────
# SAVE DATASET
# ─────────────────────────────────────────────
df.to_csv(
    "btc_expanded_features.csv",
    index=False
)

print("Expanded dataset saved successfully")
