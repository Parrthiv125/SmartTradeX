import streamlit as st


def dashboard_container(title: str, subtitle: str | None = None):
    """
    Standard dashboard page layout wrapper.
    Keeps all pages visually consistent.
    """

    st.title(title)

    if subtitle:
        st.caption(subtitle)

    st.divider()

    # return container for page content
    return st.container()
