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


# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Live Market",
    layout="wide"
)

st.title("📈 Live Market")
st.markdown("🟢 **Data Source: Binance (REAL)**")


# ─────────────────────────────────────────────
# AUTO REFRESH (every 2 seconds)
# ─────────────────────────────────────────────

st_autorefresh(interval=2000, key="live_market_refresh")


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
# Market Data (REAL BINANCE)
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
    st.info("Waiting for Binance market data...")
else:
    # -----------------------------
    # Live metrics
    # -----------------------------
    col1, col2 = st.columns(2)

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

    # -----------------------------
    # Chart (REAL + LIVE)
    # -----------------------------
    render_chart(
        candles=candles,
        markers=markers
    )

    # -----------------------------
    # Marker list
    # -----------------------------
    render_markers(markers)


st.caption("Chart uses real Binance candles with live price overlay.")
