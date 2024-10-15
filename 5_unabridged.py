import streamlit as st

st.title("Unabridged Songs")

df = st.session_state.data[st.session_state.data['Playlist'] == "Unabridged Top Songs"]
df.to_csv("data/unabridged.csv", index=False)

st.table(df)