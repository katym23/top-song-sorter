import streamlit as st
import pandas as pd

st.title("Master List")

df = st.session_state.data
df.to_csv("data/master_list.csv", index=False)

st.bar_chart(df.set_index("Title")["TotalScore"])  # Use st.bar_chart for Streamlit

st.table(df)