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

state = get_state() or {}
render_engine_controls(state)

st.divider()


# ----------------------------
# Market data
# ----------------------------
candles_resp = get_candles(interval) or {}
candles = candles_resp.get("candles", [])
markers = get_markers() or []

# cache candles so chart never disappears
if "cached_candles" not in st.session_state:
    st.session_state.cached_candles = candles

if candles:
    st.session_state.cached_candles = candles
else:
    candles = st.session_state.cached_candles

st.write("Candles count:", len(candles))


# ----------------------------
# Metrics
# ----------------------------
st.subheader("Live Market Metrics")

col1, col2 = st.columns(2)

col1.metric("BTC Live Price", get_live_price())

last_marker = markers[-1].get("type") if markers else "NONE"
col2.metric("Last Marker", last_marker)


# ----------------------------
# Chart
# ----------------------------
st.subheader("BTC Market Chart")

chart_mode = st.radio(
    "Chart Type",
    ["Line", "Candlestick"],
    horizontal=True,
)

render_chart(
    candles=candles,
    markers=markers,
    chart_mode=chart_mode,
)


# ----------------------------
# Markers
# ----------------------------
st.subheader("Recent Marker Activity")
render_markers(markers)
