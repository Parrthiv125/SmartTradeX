import streamlit as st
from streamlit_autorefresh import st_autorefresh

from services.api_client import (
    get_state,
    get_candles,
    get_markers,
    get_live_price,
)

from components.chart import render_chart
from components.marker_layer import render_markers
from components.controls import render_engine_controls
from layouts.dashboard_layout import dashboard_container


st.set_page_config(page_title="Live Market", layout="wide")

page = dashboard_container(
    "📈 Live Market",
    "🟢 Data Source: Binance (REAL)"
)

st_autorefresh(interval=2000, key="live_market_refresh")


# ----------------------------
# Timeframe selector
# ----------------------------
st.subheader("Market Settings")

interval = st.selectbox(
    "Select Timeframe",
    ["1m", "3m", "5m", "15m", "1h", "4h", "1d"],
    index=2
)


# ----------------------------
# Engine controls
# ----------------------------
st.subheader("Engine Controls")

try:
    state = get_state() or {}
    render_engine_controls(state)
except Exception as e:
    st.error("API not reachable")
    st.write(str(e))
    st.stop()


st.divider()

# ----------------------------
# Market data
# ----------------------------
candles_resp = get_candles(interval)

# IMPORTANT FIX
if not candles_resp:
    st.warning("Backend not returning candle data yet...")
    st.stop()

candles = candles_resp.get("candles", [])
markers = get_markers()

st.write("Candles count:", len(candles))   # diagnostic line


if not candles:
    st.info("Waiting for Binance market data...")
    st.stop()


# ----------------------------
# Metrics
# ----------------------------
st.subheader("Live Market Metrics")

spacer1, col1, col2, spacer2 = st.columns([1, 3, 3, 1])

with col1:
    try:
        st.metric("BTC Live Price", get_live_price())
    except:
        st.metric("BTC Live Price", "—")

with col2:
    last_marker = markers[-1].get("type") if markers else "NONE"
    st.metric("Last Marker", last_marker)


# ----------------------------
# Chart
# ----------------------------
st.subheader("BTC Market Chart")

render_chart(candles=candles, markers=markers)


# ----------------------------
# Markers
# ----------------------------
st.subheader("Recent Marker Activity")
render_markers(markers)
