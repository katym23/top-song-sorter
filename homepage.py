import streamlit as st

st.set_page_config(
    page_title="The Best Spotify Stats App Ever"
)

st.title("Main Page")
st.write("""
         Welcome to the top songs sorter. Input a song and some
         information about how you feel about it, and the app will
         score it and sort it into one of a top 100 songs playlist, an unabridged
         songs playlist, or no playlist.

         Start by heading to the inputs tab and entering some songs.
         """)