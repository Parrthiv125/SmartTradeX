# gui/app.py

import streamlit as st

st.set_page_config(page_title="SmartTradeX", layout="wide")

st.title("SmartTradeX Dashboard")

st.sidebar.title("Navigation")

st.sidebar.markdown(
    """
    Select a page from the sidebar to view:
    - Live Market
    - Paper Trading
    """
)

st.info("Use the sidebar to navigate between pages.")
# gui/app.py (example sidebar)
st.sidebar.page_link("gui/pages/live_market.py", label="Live Market")
