import streamlit as st


def render_navigation():
    """
    Global sidebar navigation for SmartTradeX.
    Only links to pages that currently exist to avoid Streamlit errors.
    """

    with st.sidebar:
        st.title("SmartTradeX")
        st.markdown("### Navigation")

        # EXISTING pages only
        st.page_link("app.py", label="Dashboard", icon="📊")
        st.page_link("pages/live_market.py", label="Live Market", icon="📈")
        st.page_link("pages/paper_trading.py", label="Paper Trading", icon="💼")
        st.page_link("pages/analytics.py", label="Analytics", icon="📉")

        st.markdown("---")
        st.caption("SmartTradeX AI Trading Platform")
