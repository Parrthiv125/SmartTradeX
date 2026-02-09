import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from services.api_client import get_live_price

WINDOW = 120  # visible candles


def render_chart(candles: list, markers: list | None = None):
    """
    Render REAL BTC chart with:
    - Line / Candlestick toggle
    - Sliding window behavior (TradingView style)
    - Live price appended
    - BUY / SELL markers
    """

    if not candles:
        st.info("Waiting for Binance market data...")
        return

    chart_mode = st.radio(
        "Chart Type",
        ["Line", "Candlestick"],
        horizontal=True,
    )

    df = pd.DataFrame(candles)
    df["time"] = pd.to_datetime(df["time"])

    # -----------------------------
    # SLIDING WINDOW
    # -----------------------------
    df = df.tail(WINDOW)

    # -----------------------------
    # Append live price
    # -----------------------------
    try:
        live_price = get_live_price()

        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    [{
                        "time": pd.Timestamp.utcnow(),
                        "open": live_price,
                        "high": live_price,
                        "low": live_price,
                        "close": live_price,
                    }]
                )
            ],
            ignore_index=True,
        )
    except Exception:
        pass

    fig = go.Figure()

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

    # markers
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
                    marker=dict(symbol="triangle-up", size=12, color="green"),
                )
            )

        if sells:
            fig.add_trace(
                go.Scatter(
                    x=[pd.to_datetime(m["time"]) for m in sells],
                    y=[m["price"] for m in sells],
                    mode="markers",
                    name="SELL",
                    marker=dict(symbol="triangle-down", size=12, color="red"),
                )
            )

    fig.update_layout(
        template="plotly_dark",
        height=520,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Time",
        yaxis_title="BTC Price",
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True)
