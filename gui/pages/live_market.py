# gui/pages/live_market.py

import streamlit as st
import time

from services.api_client import get_state
from components.chart import render_chart
from components.marker_layer import render_markers
from components.controls import render_engine_controls


# ─────────────────────────────────────────────
# Page config (MUST be first Streamlit call)
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Live Market",
    layout="wide"
)

st.title("📈 Live Market")


# ─────────────────────────────────────────────
# Live Engine State
# ─────────────────────────────────────────────

st.subheader("Live Engine State")

state_placeholder = st.empty()

try:
    # Fetch full engine state from API
    state = get_state()

    # Safely extract engine state (supports different API keys)
    engine_state = state


    # Render centralized engine controls
    render_engine_controls(engine_state)

    # If market data is not ready yet
    if not state or not state.get("market_data"):
        st.info("Waiting for market data...")

    else:
        market = state.get("market_data", {})
        candles = state.get("candles", [])
        markers = state.get("markers", [])

        with state_placeholder.container():
            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    label="BTC Price",
                    value=market.get("close", "—")
                )

            with col2:
                last_marker = (
                    markers[-1].get("action")
                    if markers and isinstance(markers[-1], dict)
                    else "NONE"
                )

                st.metric(
                    label="Last Marker",
                    value=last_marker
                )

        # ─────────────────────────────────────────────
        # Chart with markers
        # ─────────────────────────────────────────────

        render_chart(
            candles=candles,
            markers=markers
        )

        # ─────────────────────────────────────────────
        # Marker list (textual)
        # ─────────────────────────────────────────────

        render_markers(markers)

except Exception as e:
    st.error("API not reachable")
    st.write(str(e))


st.caption("Live data updates automatically while engine is running.")


# ─────────────────────────────────────────────
# Controlled polling (safe & engine-aware)
# ─────────────────────────────────────────────

if engine_state.get("running"):
    time.sleep(1)
    st.rerun()
