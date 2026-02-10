import streamlit as st
from layouts.navigation import render_navigation


def dashboard_container(title: str, subtitle: str | None = None):
    """
    Standard dashboard page layout wrapper.
    Ensures SAME sidebar across ALL pages.
    """

    # GLOBAL SIDEBAR (important)
    render_navigation()

    # PAGE HEADER
    st.title(title)

    if subtitle:
        st.caption(subtitle)

    st.divider()

    return st.container()
