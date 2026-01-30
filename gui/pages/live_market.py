# gui/pages/live_market.py

import streamlit as st
from gui.services.api_client import (
    get_engine_status,
    get_engine_config,
    get_markers,
)

st.set_page_config(page_title="Live Market", layout="wide")

st.title("Live Market")

# Poll API
try:
    status = get_engine_status()
    config = get_engine_config()
    markers = get_markers()

    st.success("API Connected")

    st.subheader("Engine Status")
    st.json(status)

    st.subheader("Engine Configuration")
    st.json(config)

    st.subheader("Trading Markers")
    st.json(markers)

except Exception as e:
    st.error("API not reachable")
    st.write(e)
