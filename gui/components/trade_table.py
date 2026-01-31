import streamlit as st
import pandas as pd

def render_trade_table(trades):
    st.subheader("Trade History")

    if not trades:
        st.info("No trades executed yet.")
        return

    df = pd.DataFrame(trades)
    st.dataframe(df, use_container_width=True)