import streamlit as st


def render_navigation():
    """
    Global sidebar navigation for SmartTradeX.
    Keeps page structure consistent.
    """

    st.sidebar.title("SmartTradeX")

    st.sidebar.markdown("### Navigation")

    st.sidebar.page_link("app.py", label="App Home")
    st.sidebar.page_link("pages/live_market.py", label="Live Market")
    st.sidebar.page_link("pages/paper_trading.py", label="Paper Trading")

    st.sidebar.markdown("---")
    st.sidebar.caption("SmartTradeX AI Trading Platform")
