import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_chart(candles: list, markers: list):
    """
    Render price chart with BUY / SELL overlays.
    GUI ONLY — no trading logic.
    """

    # -----------------------------
    # Guard: no candle data
    # -----------------------------
    if not candles:
        st.info("No market data available.")
        return

    # -----------------------------
    # Prepare candle dataframe
    # -----------------------------
    df = pd.DataFrame(candles)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    fig = go.Figure()

    # -----------------------------
    # Price line
    # -----------------------------
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["close"],
            mode="lines",
            name="Price",
            line=dict(width=2),
        )
    )

    # -----------------------------
    # SAFE marker filtering
    # (prevents chart disappearing)
    # -----------------------------
    buys = [
        m for m in markers
        if m.get("action") == "BUY"
        and m.get("price") is not None
        and m.get("timestamp") is not None
    ]

    sells = [
        m for m in markers
        if m.get("action") == "SELL"
        and m.get("price") is not None
        and m.get("timestamp") is not None
    ]

    # -----------------------------
    # BUY markers
    # -----------------------------
    if buys:
        fig.add_trace(
            go.Scatter(
                x=[pd.to_datetime(m["timestamp"], unit="ms") for m in buys],
                y=[m["price"] for m in buys],
                mode="markers",
                name="BUY",
                marker=dict(
                    symbol="triangle-up",
                    size=12,
                ),
            )
        )

    # -----------------------------
    # SELL markers
    # -----------------------------
    if sells:
        fig.add_trace(
            go.Scatter(
                x=[pd.to_datetime(m["timestamp"], unit="ms") for m in sells],
                y=[m["price"] for m in sells],
                mode="markers",
                name="SELL",
                marker=dict(
                    symbol="triangle-down",
                    size=12,
                ),
            )
        )

    # -----------------------------
    # Layout
    # -----------------------------
    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Time",
        yaxis_title="Price",
        showlegend=True,
    )

    st.plotly_chart(fig, width="stretch")

