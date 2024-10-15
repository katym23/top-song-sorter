import streamlit as st
import pandas as pd

st.title("Top 100 Songs")

df = st.session_state.data[st.session_state.data['Playlist'] == "Top 100 Songs"]
df.to_csv("data/top_100.csv", index=False)

st.table(df)