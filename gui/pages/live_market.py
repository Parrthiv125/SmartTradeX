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



# ------------------------------------------------
# Page config
# ------------------------------------------------
st.set_page_config(
    page_title="Live Market",
    layout="wide"
)

page = dashboard_container(
    "📈 Live Market",
    "🟢 Data Source: Binance (REAL)"
)


# ------------------------------------------------
# AUTO REFRESH (every 2 seconds)
# ------------------------------------------------
st_autorefresh(interval=2000, key="live_market_refresh")


# ------------------------------------------------
# Engine Controls Section
# ------------------------------------------------
st.subheader("Engine Controls")
st.caption("Engine control and current running state")

try:
    state = get_state()
    engine_state = state or {}

    # Only render controls (status handled inside controls.py)
    render_engine_controls(engine_state)

except Exception as e:
    st.error("API not reachable")
    st.write(str(e))
    st.stop()


# ------------------------------------------------
# Market Data Section
# ------------------------------------------------
st.divider()

try:
    candles_resp = get_candles()
    markers = get_markers()
    candles = candles_resp.get("candles", [])

except Exception as e:
    st.error("Market data not available")
    st.write(str(e))
    st.stop()


if not candles:
    st.info("Waiting for Binance market data...")
else:

    # ------------------------------------------------
    # Metrics Section
    # ------------------------------------------------
    st.subheader("Live Market Metrics")

    spacer1, col1, col2, spacer2 = st.columns([1, 3, 3, 1])

    with col1:
        try:
            live_price = get_live_price()
            st.metric(
                label="BTC Live Price",
                value=live_price
            )
        except Exception:
            st.metric(
                label="BTC Live Price",
                value="—"
            )

    with col2:
        last_marker = markers[-1].get("type") if markers else "NONE"
        st.metric(
            label="Last Marker",
            value=last_marker
        )

    # ------------------------------------------------
    # Chart Section
    # ------------------------------------------------
    st.subheader("BTC Market Chart")

    render_chart(
        candles=candles,
        markers=markers
    )

    # ------------------------------------------------
    # Marker Activity Section
    # ------------------------------------------------
    st.subheader("Recent Marker Activity")

    render_markers(markers)


st.caption("Chart uses real Binance candles with live price overlay.")
