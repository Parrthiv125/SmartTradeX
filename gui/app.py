import streamlit as st
import pandas as pd
import time

from layouts.dashboard_layout import dashboard_container
from services.api_client import get_candles

st.set_page_config(page_title="SmartTradeX", layout="wide")

dashboard_container(
    "📊 SmartTradeX — Dashboard",
    "System Overview"
)

kpi_placeholder = st.empty()
chart_placeholder = st.empty()

while True:

    candles_data = get_candles()
    candles = candles_data.get("candles", [])

    if candles:
        df = pd.DataFrame(candles)
        price = round(df["close"].iloc[-1], 2)
    else:
        df = pd.DataFrame()
        price = "-"

    # KPI ROW (REFERENCE SPACING)
    with kpi_placeholder.container():

        st.markdown("###")

        k1, k2, k3, k4 = st.columns(4, gap="large")

        with k1:
            st.metric("BTC/USDT Price", price)

        with k2:
            st.metric("Engine Status", "Stopped")

        with k3:
            st.metric("Last Prediction", "—")

        with k4:
            st.metric("Prediction Accuracy", "—")

        st.markdown("###")

    # CHART PANEL
    with chart_placeholder.container():

        st.divider()

        chart_col, stats_col = st.columns([4, 1], gap="large")

        with chart_col:
            st.subheader("BTC Price Trend")
            if not df.empty:
                st.line_chart(df["close"])

        with stats_col:
            st.subheader("Quick Stats")
            st.write("Last Update:", time.strftime("%H:%M:%S"))
            st.write("Today's Trades: —")
            st.write("Predictions Today: —")
            st.write("System Latency: —")

    time.sleep(2)
