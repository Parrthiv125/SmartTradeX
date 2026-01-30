# gui/components/trade_table.py

import streamlit as st


def render_trade_table(trades: list):
    """
    Render a table of executed paper trades.
    """
    st.subheader("Trade Table")

    if not trades:
        st.info("No trades executed yet.")
        return

    st.table(trades)
