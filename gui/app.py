import streamlit as st
import pandas as pd

from layouts.navigation import render_navigation

from services.api_client import (
    get_candles,
    get_markers,
    get_trades,
    start_engine,
    stop_engine,
)

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(page_title="SmartTradeX", layout="wide")

# --------------------------------
# LOAD CUSTOM SIDEBAR
# --------------------------------
render_navigation()

# --------------------------------
# Session state for engine status
# --------------------------------
if "engine_running" not in st.session_state:
    st.session_state.engine_running = False

# --------------------------------
# PAGE HEADER
# --------------------------------
st.title("📈 SmartTradeX — Paper Trading Dashboard")

# --------------------------------
# Control buttons
# --------------------------------
col1, col2 = st.columns(2)

if col1.button("▶ Start Trader"):
    start_engine()
    st.session_state.engine_running = True

if col2.button("⏹ Stop Trader"):
    stop_engine()
    st.session_state.engine_running = False

# --------------------------------
# Engine Status Indicator
# --------------------------------
if st.session_state.engine_running:
    st.success("🟢 Engine Running")
else:
    st.error("🔴 Engine Stopped")

st.divider()

# --------------------------------
# Market candles
# --------------------------------
st.subheader("Market Candles")

candles_data = get_candles()
candles = candles_data.get("candles", [])

if candles:
    df_candles = pd.DataFrame(candles)
    st.dataframe(df_candles, use_container_width=True)
else:
    st.info("No candle data available")

# --------------------------------
# Markers
# --------------------------------
st.subheader("Markers")
markers = get_markers()
st.json(markers)

# --------------------------------
# Trades
# --------------------------------
st.subheader("Trades")

trades = get_trades()

if trades:
    df_trades = pd.DataFrame(trades)
    st.dataframe(df_trades, use_container_width=True)
else:
    st.info("No trades available")
