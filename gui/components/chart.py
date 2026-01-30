import streamlit as st
import pandas as pd


def render_chart(candles: list):
    if not candles:
        st.info("Waiting for market data...")
        return

    df = pd.DataFrame(candles)

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

    st.line_chart(df["close"])
