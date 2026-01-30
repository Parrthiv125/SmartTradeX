# gui/pages/live_market.py

import streamlit as st
from components.marker_layer import render_markers
from components.chart import render_chart
import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"
START_URL = f"{API_BASE}/engine/start"
STOP_URL = f"{API_BASE}/engine/stop"
RESET_URL = f"{API_BASE}/engine/reset"
STATUS_URL = f"{API_BASE}/engine/status"
st.subheader("Engine Controls")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("▶ Start"):
        try:
            r = requests.post(START_URL, timeout=5)
            st.success(r.json().get("message", "Started"))
        except Exception as e:
            st.error(f"Start failed: {e}")

with c2:
    if st.button("⏸ Stop"):
        try:
            r = requests.post(STOP_URL, timeout=5)
            st.success(r.json().get("message", "Stopped"))
        except Exception as e:
            st.error(f"Stop failed: {e}")

with c3:
    if st.button("♻ Reset"):
        try:
            r = requests.post(RESET_URL, timeout=5)
            st.success(r.json().get("message", "Reset"))
        except Exception as e:
            st.error(f"Reset failed: {e}")
st.subheader("Engine Status")
try:
    status = requests.get(STATUS_URL, timeout=5).json()
    st.json(status)
except Exception as e:
    st.error(f"API not reachable: {e}")



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

render_chart()

