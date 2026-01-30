# gui/pages/live_market.py

import streamlit as st
from components.marker_layer import render_markers

from services.api_client import (
    get_engine_status,
    get_engine_config,
    get_markers,
)

st.set_page_config(page_title="Live Market", layout="wide")

st.title("Live Market")

def safe_render(title: str, data):
    st.subheader(title)
    if not data:
        st.info("No data available.")
    else:
        st.json(data)

try:
    status = get_engine_status()
    config = get_engine_config()
    markers = get_markers()

    st.success("API Connected")

    safe_render("Engine Status", status)
    safe_render("Engine Configuration", config)
    render_markers(markers.get("markers", []))

except Exception as e:
    st.error("API not reachable")
    st.write(str(e))
