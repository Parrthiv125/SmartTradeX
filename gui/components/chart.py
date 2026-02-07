import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from services.api_client import get_live_price


def render_chart(candles: list, markers: list | None = None):
    """
    Render REAL Binance price chart with:
    - Closed candle prices
    - Live Binance price overlay
    - BUY / SELL markers
    """

    # -----------------------------
    # Guard: no candle data
    # -----------------------------
    if not candles:
        st.info("Waiting for Binance market data...")
        return

    # -----------------------------
    # Prepare candle dataframe
    # -----------------------------
    df = pd.DataFrame(candles)

    # Binance provides ISO timestamps in `time`
    df["time"] = pd.to_datetime(df["time"])

    fig = go.Figure()

    # -----------------------------
    # Closed candle price line
    # -----------------------------
    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["close"],
            mode="lines",
            name="Binance (closed candles)",
            line=dict(width=2, color="#1f77b4"),
        )
    )

    # -----------------------------
    # Live Binance price overlay
    # -----------------------------
    try:
        live_price = get_live_price()

        fig.add_hline(
            y=live_price,
            line_dash="dot",
            line_color="yellow",
            annotation_text=f"Live Price: {live_price}",
            annotation_position="top left",
        )
    except Exception:
        # Live price unavailable → chart still works
        pass

    # -----------------------------
    # BUY / SELL markers
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
        height=520,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Time",
        yaxis_title="Price",
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True)
