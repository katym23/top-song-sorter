import streamlit as st
import pandas as pd
import datetime

st.table(st.session_state.data)

path = "C:/Users/katym/OneDrive/Documents/OneDrive/Python/NewKatyPy/Katys_Independent_DA_Projects/top_songs_202/SongInputs.xlsx"

# Function to delete a song by title and artist
def delete_song_by_title_artist(selected_title, selected_artist):
    if selected_title and selected_artist:
        # Filter out the selected song by both title and artist
        st.session_state.data = st.session_state.data[
            ~((st.session_state.data["Title"] == selected_title) & 
              (st.session_state.data["Artist"] == selected_artist))
        ].reset_index(drop=True)
        st.session_state.data.to_excel(path, index=False)
        st.success(f"Song '{selected_title}' by {selected_artist} deleted successfully!")
    else:
        st.error("No song selected for deletion.")

# Deletion form - select by song title and artist
with st.form("Delete Songs"):
    song_titles = st.session_state.data['Title'].unique().tolist()
    selected_title = st.selectbox("Select the song title", options=song_titles, key="title_select")

    # Show all unique artists from the data regardless of the selected song
    all_artists = st.session_state.data['Artist'].unique().tolist()
    selected_artist = st.selectbox("Select the artist", options=all_artists, key="artist_select")

    # Add a submit button to trigger the deletion function
    delete_button = st.form_submit_button("Delete Song")

# Perform the deletion if the submit button is pressed
if delete_button and selected_title and selected_artist:
    delete_song_by_title_artist(selected_title, selected_artist)

# Display the current state of the DataFrame
st.table(st.session_state.data)