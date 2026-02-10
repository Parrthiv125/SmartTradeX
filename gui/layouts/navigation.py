import streamlit as st


def render_navigation():
    """
    Global sidebar navigation for SmartTradeX
    Production terminal layout
    """

    with st.sidebar:
        st.title("SmartTradeX")
        st.markdown("### Navigation")

        st.page_link("app.py", label="Dashboard", icon="📊")
        st.page_link("pages/live_market.py", label="Live Market", icon="📈")
        st.page_link("pages/paper_trading.py", label="Paper Trading", icon="💼")

        st.markdown("---")
        st.caption("SmartTradeX AI Trading Platform")
