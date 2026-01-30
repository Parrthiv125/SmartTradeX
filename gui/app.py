# gui/app.py

import streamlit as st

st.set_page_config(
    page_title="SmartTradeX",
    layout="wide"
)

st.title("SmartTradeX Dashboard")

st.markdown(
    """
    ### Welcome to SmartTradeX 🚀

    Use the **sidebar** to navigate between:
    - **Live Market**
    - **Paper Trading**
    """
)

st.info("Select a page from the sidebar to get started.")
