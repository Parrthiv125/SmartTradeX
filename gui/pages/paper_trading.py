# gui/pages/paper_trading.py

import streamlit as st
from components.trade_table import render_trade_table
from components.metrics import render_metrics


from services.api_client import (
    get_positions,
    get_trades,
    get_pnl,
)

st.set_page_config(page_title="Paper Trading", layout="wide")

st.title("Paper Trading")

def safe_render(title: str, data):
    st.subheader(title)
    if not data:
        st.info("No data available.")
    else:
        st.json(data)

try:
    positions = get_positions()
    trades = get_trades()
    pnl = get_pnl()

    st.success("API Connected")

    safe_render("Open Positions", positions.get("positions", []))
    # safe_render("Trade History", trades.get("trades", []))
    render_trade_table(trades.get("trades", []))
    render_metrics(pnl.get("pnl", {}))


except Exception as e:
    st.error("API not reachable")
    st.write(str(e))
