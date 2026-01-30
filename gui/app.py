# gui/app.py

import streamlit as st
import requests

st.set_page_config(page_title="SmartTradeX", layout="wide")

st.title("SmartTradeX Dashboard")

STATUS_URL = "http://127.0.0.1:8000/engine/status"
CONFIG_URL = "http://127.0.0.1:8000/engine/config"

try:
    status_resp = requests.get(STATUS_URL)
    config_resp = requests.get(CONFIG_URL)

    st.success("API Connected")

    st.subheader("Engine Status")
    st.json(status_resp.json())

    st.subheader("Engine Configuration")
    st.json(config_resp.json())

except Exception as e:
    st.error("API not reachable")
    st.write(e)
