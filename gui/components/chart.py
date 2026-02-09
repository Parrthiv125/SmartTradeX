import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def render_chart(candles: list, markers: list | None = None, chart_mode="Line"):

    if not candles:
        st.warning("No candle data yet...")
        return

    df = pd.DataFrame(candles)

    # ensure correct types
    df["time"] = pd.to_datetime(df["time"])
    df["open"] = df["open"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["close"] = df["close"].astype(float)

    fig = go.Figure()

    # ---------- line ----------
    if chart_mode == "Line":
        fig.add_trace(
            go.Scatter(
                x=df["time"],
                y=df["close"],
                mode="lines",
                name="BTC Price",
            )
        )

    # ---------- candle ----------
    else:
        fig.add_trace(
            go.Candlestick(
                x=df["time"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="BTC Candles",
            )
        )

    # ---------- marker filter (IMPORTANT FIX) ----------
    if markers:
        min_price = df["low"].min()
        max_price = df["high"].max()

        buy_x, buy_y, sell_x, sell_y = [], [], [], []

        for m in markers:
            price = float(m["price"])

            # ignore markers far outside chart range
            if price < min_price * 0.7 or price > max_price * 1.3:
                continue

            if m.get("type") == "BUY":
                buy_x.append(m["time"])
                buy_y.append(price)

            if m.get("type") == "SELL":
                sell_x.append(m["time"])
                sell_y.append(price)

        if buy_x:
            fig.add_trace(
                go.Scatter(
                    x=buy_x,
                    y=buy_y,
                    mode="markers",
                    marker=dict(symbol="triangle-up", size=12),
                    name="BUY",
                )
            )

        if sell_x:
            fig.add_trace(
                go.Scatter(
                    x=sell_x,
                    y=sell_y,
                    mode="markers",
                    marker=dict(symbol="triangle-down", size=12),
                    name="SELL",
                )
            )

    fig.update_layout(
        template="plotly_dark",
        height=520,
        margin=dict(l=10, r=10, t=30, b=10),
    )

    st.plotly_chart(fig, width="stretch")
