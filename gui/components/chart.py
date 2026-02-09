import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def render_chart(candles: list, markers: list | None = None, chart_mode="Line"):

    # ---------- SAFETY ----------
    if candles is None or len(candles) == 0:
        st.warning("No candle data yet...")
        return

    df = pd.DataFrame(candles)

    # ---------- FIX TIME ----------
    # backend gives milliseconds timestamp
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"], unit="ms")
    elif "timestamp" in df.columns:
        df["time"] = pd.to_datetime(df["timestamp"], unit="ms")

    # numeric conversion
    df["open"] = df["open"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["close"] = df["close"].astype(float)

    df = df.sort_values("time")

    fig = go.Figure()

    # ---------- LINE ----------
    if chart_mode == "Line":
        fig.add_trace(
            go.Scatter(
                x=df["time"],
                y=df["close"],
                mode="lines",
                name="BTC Price",
                line=dict(width=2),
            )
        )

    # ---------- CANDLE ----------
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

    # ---------- MARKERS ----------
    if markers:
        buy_x, buy_y, sell_x, sell_y = [], [], [], []

        for m in markers:
            t = pd.to_datetime(m["time"])
            price = float(m["price"])

            if m.get("type") == "BUY":
                buy_x.append(t)
                buy_y.append(price)

            if m.get("type") == "SELL":
                sell_x.append(t)
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
        xaxis_title="Time",
        yaxis_title="Price"
    )

    st.plotly_chart(fig, width="stretch")
