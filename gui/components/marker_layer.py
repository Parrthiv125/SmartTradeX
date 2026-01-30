# gui/components/marker_layer.py

import streamlit as st


def render_markers(markers: list):
    """
    Render trading markers (BUY / SELL / HOLD).
    """
    st.subheader("Markers")

    if not markers:
        st.info("No markers available.")
        return

    for marker in markers:
        st.write(marker)
