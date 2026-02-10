import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_chart(candles, markers=None, chart_mode="Candlestick"):
    """
    Render BTC chart using real timestamps
    Optimized for realtime perception
    """

    if not candles:
        st.warning("No candle data available")
        return

    # -------------------------
    # Dataframe preparation
    # -------------------------
    df = pd.DataFrame(candles)

    df["time"] = pd.to_datetime(df["time"], unit="ms", errors="coerce")
    df = df.dropna(subset=["time"])
    df = df.sort_values("time")

    # -------------------------
    # Chart base
    # -------------------------
    if chart_mode == "Line":
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=df["time"],
                    y=df["close"],
                    mode="lines",
                    name="BTC Price",
                )
            ]
        )
    else:
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df["time"],
                    open=df["open"],
                    high=df["high"],
                    low=df["low"],
                    close=df["close"],
                    name="BTC",
                )
            ]
        )

    # -------------------------
    # Markers
    # -------------------------
    if markers:
        mdf = pd.DataFrame(markers)

        if not mdf.empty:
            mdf["time"] = pd.to_datetime(mdf["time"], unit="ms", errors="coerce")

            fig.add_trace(
                go.Scatter(
                    x=mdf["time"],
                    y=mdf["price"],
                    mode="markers",
                    marker=dict(size=9),
                    name="Signals",
                )
            )

    # -------------------------
    # Auto-scroll to latest candle
    # -------------------------
    last_time = df["time"].iloc[-1]
    first_visible = df["time"].iloc[-120] if len(df) > 120 else df["time"].iloc[0]

    fig.update_xaxes(range=[first_visible, last_time])

    # -------------------------
    # Layout
    # -------------------------
    fig.update_layout(
        height=600,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Time",
        yaxis_title="BTC Price",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
    )

    st.plotly_chart(fig, use_container_width=True)
