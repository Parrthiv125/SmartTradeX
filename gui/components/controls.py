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

    # -------- STATUS BAR ----------
    if running:
        st.success("🟢 Engine Running")
    else:
        st.warning("🔴 Engine Stopped")

    st.divider()

    c1, c2, c3 = st.columns(3)

    # -------- START ----------
    with c1:
        if st.button("▶ Start Engine", disabled=running):
            with st.spinner("Starting engine..."):
                ok = start_engine()

            if ok:
                st.success("Engine start request sent")
            else:
                st.error("Failed to start engine")

            st.rerun()

    # -------- STOP ----------
    with c2:
        if st.button("⏸ Stop Engine", disabled=not running):
            with st.spinner("Stopping engine..."):
                ok = stop_engine()

            if ok:
                st.success("Engine stop request sent")
            else:
                st.error("Failed to stop engine")

            st.rerun()

    # -------- RESET ----------
    with c3:
        if st.button("♻ Reset Engine"):
            with st.spinner("Resetting engine..."):
                ok = reset_engine()

            if ok:
                st.success("Engine reset request sent")
            else:
                st.error("Failed to reset engine")

            st.rerun()
