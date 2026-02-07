import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_chart(candles: list, markers: list | None = None):
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

    # ✅ FIX: backend provides `time`, not `timestamp`
    df["time"] = pd.to_datetime(df["time"])

    fig = go.Figure()

    # -----------------------------
    # Price line
    # -----------------------------
    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["close"],
            mode="lines",
            name="Price",
            line=dict(width=2),
        )
    )

    # -----------------------------
    # Marker overlays (SAFE)
    # -----------------------------
    if markers:
        buys = [m for m in markers if m.get("type") == "BUY"]
        sells = [m for m in markers if m.get("type") == "SELL"]

        if buys:
            fig.add_trace(
                go.Scatter(
                    x=[pd.to_datetime(m["time"]) for m in buys],
                    y=[m["price"] for m in buys],
                    mode="markers",
                    name="BUY",
                    marker=dict(
                        symbol="triangle-up",
                        size=12,
                        color="green",
                    ),
                )
            )

        if sells:
            fig.add_trace(
                go.Scatter(
                    x=[pd.to_datetime(m["time"]) for m in sells],
                    y=[m["price"] for m in sells],
                    mode="markers",
                    name="SELL",
                    marker=dict(
                        symbol="triangle-down",
                        size=12,
                        color="red",
                    ),
                )
            )

    # -----------------------------
    # Layout
    # -----------------------------
    fig.update_layout(
        template="plotly_dark",
        height=500,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Time",
        yaxis_title="Price",
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True)
