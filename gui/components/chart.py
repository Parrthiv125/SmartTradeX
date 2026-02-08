import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from services.api_client import get_live_price


def render_chart(candles: list, markers: list | None = None):
    """
    Render REAL live BTC price line chart with:
    - Historical candle close prices
    - Live price appended as last point (smooth live line)
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
    df["time"] = pd.to_datetime(df["time"])

    # -----------------------------
    # Append LIVE price as last point
    # -----------------------------
    try:
        live_price = get_live_price()

        live_row = {
            "time": pd.Timestamp.utcnow(),
            "close": live_price,
        }

        df = pd.concat(
            [df, pd.DataFrame([live_row])],
            ignore_index=True
        )

    except Exception:
        # Live price unavailable → continue with candle data only
        live_price = None

    # -----------------------------
    # Build chart
    # -----------------------------
    fig = go.Figure()

    # Smooth continuous live line
    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["close"],
            mode="lines",
            name="BTC Price (Live)",
            line=dict(
                width=2,
                color="#4da6ff",
            ),
        )
    )

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
        yaxis_title="BTC Price",
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True)
