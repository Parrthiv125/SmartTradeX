import streamlit as st

from services.api_client import (
    start_engine,
    stop_engine,
    reset_engine,
)


def render_engine_controls(engine_state):
    """
    GUI-only engine control panel.
    No trading or engine logic here.
    """

    running = engine_state.get("running", False)

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(
            "▶ Start Engine",
            disabled=running
        ):
            start_engine()
            st.success("Engine started")

    with c2:
        if st.button(
            "⏸ Stop Engine",
            disabled=not running
        ):
            stop_engine()
            st.warning("Engine stopped")

    with c3:
        if st.button("♻ Reset Engine"):
            reset_engine()
            st.info("Engine reset")
