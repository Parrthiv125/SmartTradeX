# gui/pages/live_market.py

import streamlit as st
import time

from services.api_client import (
    start_engine,
    stop_engine,
    reset_engine,
    get_state,
)

from components.chart import render_chart
from components.marker_layer import render_markers

# ─────────────────────────────────────────────
# Page config (MUST be first)
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Live Market",
    layout="wide"
)

st.title("📈 Live Market")

# ─────────────────────────────────────────────
# Engine controls
# ─────────────────────────────────────────────

st.subheader("Engine Controls")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("▶ Start Engine"):
        start_engine()
        st.success("Engine started")

with c2:
    if st.button("⏸ Stop Engine"):
        stop_engine()
        st.warning("Engine stopped")

with c3:
    if st.button("♻ Reset Engine"):
        reset_engine()
        st.info("Engine reset")

# ─────────────────────────────────────────────
# Live state polling
# ─────────────────────────────────────────────

st.subheader("Live Engine State")

state_placeholder = st.empty()

# Poll once per rerun (Streamlit reruns automatically)
try:
    state = get_state()

    if not state or not state.get("market_data"):
        st.info("Waiting for market data...")
    else:
        market = state["market_data"]
        markers = state.get("markers", [])

        with state_placeholder.container():
            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    label="BTC Price",
                    value=market["close"]
                )

            with col2:
                last_marker = markers[-1]["action"] if markers else "NONE"
                st.metric(
                    label="Last Marker",
                    value=last_marker
                )

        # Render visuals
        candles = state.get("candles", [])
        render_chart(candles)
        render_markers(markers)


except Exception as e:
    st.error("API not reachable")
    st.write(str(e))

st.caption("Live data updates automatically while engine is running.")

time.sleep(1)
st.rerun()
