# gui/components/metrics.py

import streamlit as st


def render_metrics(pnl: dict):
    """
    Render PnL metrics.
    """
    st.subheader("PnL Metrics")

    if not pnl:
        st.info("No PnL data available.")
        return

    realized = pnl.get("realized", 0)
    unrealized = pnl.get("unrealized", 0)
    total = pnl.get("total", 0)

    col1, col2, col3 = st.columns(3)

    col1.metric("Realized PnL", realized)
    col2.metric("Unrealized PnL", unrealized)
    col3.metric("Total PnL", total)
