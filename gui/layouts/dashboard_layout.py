import streamlit as st
from layouts.navigation import render_navigation


def dashboard_container(title: str, subtitle: str | None = None):

    render_navigation()

    st.markdown("""
    <style>

    /* KPI CARD */
    [data-testid="metric-container"] {
        background: linear-gradient(180deg,#0b1220,#020617);
        border: 1px solid #273244;
        padding: 26px;
        border-radius: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        margin-bottom: 10px;
    }

    /* PANEL CARD */
    .dashboard-panel {
        background: linear-gradient(180deg,#020617,#020617);
        border: 1px solid #1f2937;
        padding: 26px;
        border-radius: 18px;
        box-shadow: 0 10px 28px rgba(0,0,0,0.35);
        margin-bottom: 20px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.title(title)

    if subtitle:
        st.caption(subtitle)

    st.divider()


def open_panel():
    st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)


def close_panel():
    st.markdown('</div>', unsafe_allow_html=True)
