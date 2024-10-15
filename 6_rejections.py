import streamlit as st

st.title("Rejected Songs")

df = st.session_state.data[st.session_state.data['Playlist'] == "None"]
df.to_csv("data/rejected_songs.csv", index=False)

st.table(df)