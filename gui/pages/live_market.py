import streamlit as st
from streamlit_autorefresh import st_autorefresh

from services.api_client import (
    get_state,
    get_candles,
    get_last_candle,
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

# ---------------------------------------
# Stable refresh loop
# ---------------------------------------
st_autorefresh(interval=2000, key="live_market_refresh")


# ---------------------------------------
# Timeframe selector
# ---------------------------------------
st.subheader("Market Settings")

interval = st.selectbox(
    "Select Timeframe",
    ["1m", "3m", "5m", "15m", "1h", "4h", "1d"],
    index=2,
    key="interval_select"
)


# ---------------------------------------
# Engine controls
# ---------------------------------------
st.subheader("Engine Controls")

state = get_state() or {}
render_engine_controls(state)

st.divider()


# ---------------------------------------
# Candle streaming buffer
# ---------------------------------------
if "candle_buffer" not in st.session_state:
    st.session_state.candle_buffer = []
    st.session_state.last_interval = interval


# Load history once OR when timeframe changes
if not st.session_state.candle_buffer or st.session_state.last_interval != interval:
    candles_resp = get_candles(interval) or {}
    st.session_state.candle_buffer = candles_resp.get("candles", [])
    st.session_state.last_interval = interval

else:
    # Only update last candle
    last_candle = get_last_candle(interval)
    if last_candle:
        if len(st.session_state.candle_buffer) > 0:
            st.session_state.candle_buffer[-1] = last_candle
        else:
            st.session_state.candle_buffer.append(last_candle)

candles = st.session_state.candle_buffer
markers = get_markers() or []

st.caption(f"Candles count: {len(candles)}")


# ---------------------------------------
# Metrics
# ---------------------------------------
st.subheader("Live Market Metrics")

col1, col2 = st.columns(2)

col1.metric("BTC Live Price", get_live_price())

last_marker = markers[-1].get("type") if markers else "NONE"
col2.metric("Last Marker", last_marker)


# ---------------------------------------
# Chart
# ---------------------------------------
st.subheader("BTC Market Chart")

chart_mode = st.radio(
    "Chart Type",
    ["Line", "Candlestick"],
    horizontal=True,
    key="chart_mode"
)

render_chart(
    candles=candles,
    markers=markers,
    chart_mode=chart_mode,
)


# ---------------------------------------
# Markers
# ---------------------------------------
st.subheader("Recent Marker Activity")
render_markers(markers)
