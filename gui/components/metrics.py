import streamlit as st


def render_position_status(position):
    """
    Visual-only component.
    Shows current active position status.
    """

    st.subheader("Active Position")

    if not position:
        st.success("No active position")
        return

    side = position.get("side", "—")
    entry_price = position.get("entry_price", 0.0)
    pnl_pct = position.get("pnl_pct", 0.0)
    hold_time = position.get("hold_time_sec", 0)

    # Color PnL text
    pnl_color = "green" if pnl_pct > 0 else "red" if pnl_pct < 0 else "gray"

    st.markdown(
        f"""
        <div style="padding: 10px; border: 1px solid #444; border-radius: 6px;">
            <strong>Status:</strong> OPEN<br>
            <strong>Side:</strong> {side}<br>
            <strong>Entry Price:</strong> {entry_price}<br>
            <strong>PnL:</strong>
            <span style="color:{pnl_color};">{pnl_pct:.2f}%</span><br>
            <strong>Hold Time:</strong> {hold_time}s
        </div>
        """,
        unsafe_allow_html=True
    )
