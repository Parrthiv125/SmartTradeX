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

    # Render table manually to allow row coloring
    for trade in trades:
        row_style = get_trade_row_color(trade)

        symbol = trade.get("symbol", "")
        side = trade.get("side", "")
        pnl = trade.get("pnl_pct", 0.0)

        reason = trade.get("exit_reason", "—")
        hold_time = trade.get("hold_time_sec", 0)

        st.markdown(
            f"""
            <div style="{row_style} padding: 6px; border-bottom: 1px solid #ddd;">
                <strong>{symbol}</strong> |
                {side} |
                {pnl:.2f}% |
                {reason} |
                {hold_time}s
            </div>
            """,
            unsafe_allow_html=True
        )
