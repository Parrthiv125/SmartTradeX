# gui/components/chart.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_chart(candles: list, markers: list):
    """
    Render price chart with BUY / SELL overlays.
    """

    if not candles:
        st.info("No market data available.")
        return

    # --- Price Data ---
    df = pd.DataFrame(candles)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["close"],
            mode="lines",
            name="Price",
            line=dict(width=2),
        )
    )

    # --- Marker Overlay ---
    buys = [m for m in markers if m["action"] == "BUY"]
    sells = [m for m in markers if m["action"] == "SELL"]

    if buys:
        fig.add_trace(
            go.Scatter(
                x=[pd.to_datetime(m["timestamp"], unit="ms") for m in buys],
                y=[m["price"] for m in buys],
                mode="markers",
                name="BUY",
                marker=dict(symbol="triangle-up", size=12),
            )
        )

    if sells:
        fig.add_trace(
            go.Scatter(
                x=[pd.to_datetime(m["timestamp"], unit="ms") for m in sells],
                y=[m["price"] for m in sells],
                mode="markers",
                name="SELL",
                marker=dict(symbol="triangle-down", size=12),
            )
        )

    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Time",
        yaxis_title="Price",
        showlegend=True,
    )

    st.plotly_chart(fig, width="stretch")
