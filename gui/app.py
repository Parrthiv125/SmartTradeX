# gui/app.py

import streamlit as st
import requests

st.set_page_config(page_title="SmartTradeX", layout="wide")

st.title("SmartTradeX Dashboard")

# Call API
API_URL = "http://127.0.0.1:8000/engine/status"

try:
    response = requests.get(API_URL)
    data = response.json()
    st.success("API Connected")
    st.json(data)
except Exception as e:
    st.error("API not reachable")
    st.write(e)