import streamlit as st
import pandas as pd


def get_trade_row_color(trade):
    """
    Decide row background color based on trade PnL.
    VISUAL ONLY. No trading logic.
    """
    pnl = trade.get("pnl_pct")

    if pnl is None:
        return ""

    if pnl > 0:
        return "background-color: #e6fffa;"  # light green
    elif pnl < 0:
        return "background-color: #ffe6e6;"  # light red
    else:
        return ""


def render_trade_table(trades):
    st.subheader("Trade History")

    if not trades:
        st.info("No trades executed yet.")
        return

    for trade in trades:
        symbol = trade.get("symbol", "")
        side = trade.get("side", "")
        pnl = trade.get("pnl_pct", 0.0)
        reason = trade.get("exit_reason", "—")
        hold_time = trade.get("hold_time_sec", 0)
        trade_time = trade.get("exit_time")

        if st.button(
            f"{symbol} | {side} | {pnl:.2f}% | {reason} | {hold_time}s",
            key=f"trade_{trade.get('trade_id', trade_time)}"
        ):
            st.session_state["selected_trade_time"] = trade_time
