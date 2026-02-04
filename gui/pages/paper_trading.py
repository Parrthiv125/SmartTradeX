# gui/pages/paper_trading.py

import streamlit as st

from components.trade_table import render_trade_table
from components.metrics import render_position_status
from services.api_client import get_trades, get_positions

st.set_page_config(page_title="Paper Trading", layout="wide")

st.title("Paper Trading")

# -----------------------------
# ACTIVE POSITION STATUS
# -----------------------------
try:
    position = get_positions()
    render_position_status(position)
except Exception as e:
    st.error("Could not fetch position status")
    st.write(str(e))

st.divider()

# -----------------------------
# TRADE HISTORY
# -----------------------------
try:
    trades = get_trades()
    st.success("API Connected")
    render_trade_table(trades)
except Exception as e:
    st.error("API not reachable")
    st.write(str(e))
