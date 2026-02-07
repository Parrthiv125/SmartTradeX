import streamlit as st
import time

from services.api_client import (
    get_state,
    get_candles,
    get_markers,
)

from components.chart import render_chart
from components.marker_layer import render_markers
from components.controls import render_engine_controls


# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Live Market",
    layout="wide"
)

st.title("📈 Live Market")


# ─────────────────────────────────────────────
# Engine State (ONLY engine info)
# ─────────────────────────────────────────────

st.subheader("Live Engine State")

try:
    state = get_state()
    engine_state = state or {}

    render_engine_controls(engine_state)

except Exception as e:
    st.error("API not reachable")
    st.write(str(e))
    st.stop()


# ─────────────────────────────────────────────
# Market Data (SEPARATE, CORRECT)
# ─────────────────────────────────────────────

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
    st.info("Waiting for market data...")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="BTC Price",
            value=candles[-1].get("close", "—")
        )

    with col2:
        last_marker = (
            markers[-1].get("type")
            if markers else "NONE"
        )

        st.metric(
            label="Last Marker",
            value=last_marker
        )

    # ─────────────────────────────────────────────
    # Chart with markers (RESTORED)
    # ─────────────────────────────────────────────

    render_chart(
        candles=candles,
        markers=markers
    )

    # ─────────────────────────────────────────────
    # Marker list
    # ─────────────────────────────────────────────

    render_markers(markers)


st.caption("Live data updates automatically while engine is running.")


# ─────────────────────────────────────────────
# Controlled auto-refresh
# ─────────────────────────────────────────────

if engine_state.get("running"):
    time.sleep(1)
    st.rerun()
