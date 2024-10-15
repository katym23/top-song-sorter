import streamlit as st
import pandas as pd
import datetime
import os, json

st.title("Add A Song")

slider_values_path = "data/thresholds.json"

# Function to calculate the total score
def calculate_total_score(date_added_input, is_chokehold_input, emotional_input, banger_input, is_iconic_input, is_listened_input):
    monthAdded = pd.to_datetime(date_added_input).month

    if monthAdded == 12:
        monthScore = 0.5
    elif monthAdded in range(1, 10):
        monthScore = 1
    else:
        monthScore = 1.3

    chokeholdScore = is_chokehold_input * 4
    emotionalScore = emotional_input
    bangerScore = banger_input * 0.8
    iconicScore = is_iconic_input * 0.7

    if (is_listened_input == 1) & (monthAdded == 12):
        stillListenScore = is_listened_input * 2
    elif (is_listened_input == 1) & (monthAdded in range(10, 12)):
        stillListenScore = is_listened_input * 0.7
    else:
        stillListenScore = is_listened_input

    totalScore = round((monthScore + chokeholdScore + emotionalScore + bangerScore + iconicScore + stillListenScore), 2)
    return totalScore

# Function to assign the playlist based on thresholds
def playlist_assignment(totalScore, song_input, is_day6_input, top_100_threshold_input, unabridged_threshold_input):
    if song_input == "NCT 127":
        playlist = "None"
    elif is_day6_input == 1:
        playlist = "Unabridged Top Songs"
    elif totalScore > top_100_threshold_input:
        playlist = "Top 100 Songs"
    elif totalScore > unabridged_threshold_input:
        playlist = "Unabridged Top Songs"
    else:
        playlist = "None"
    return playlist

# Load slider values from file if they exist
def load_slider_values():
    if os.path.exists(slider_values_path):
        with open(slider_values_path, "r") as file:
            return json.load(file)
    return {"top_100_threshold": 0.0, "unabridged_threshold": 0.0}  # Default values if file doesn't exist

# Save slider values to file
def save_slider_values(top_100_threshold, unabridged_threshold):
    with open(slider_values_path, "w") as file:
        json.dump({"top_100_threshold": top_100_threshold, "unabridged_threshold": unabridged_threshold}, file)

# Load the previous slider values (if any)
slider_values = load_slider_values()

path = "C:/Users/katym/OneDrive/Documents/OneDrive/Python/NewKatyPy/Katys_Independent_DA_Projects/top_songs_202/SongInputs.xlsx"

if 'data' not in st.session_state:
    st.session_state.data = pd.read_excel(path)

# Sliders for threshold inputs
top_100_threshold_input = st.slider("Pick a threshold for your top 100 songs playlist", 
                                    min_value=0.0, max_value=17.0, value=slider_values['top_100_threshold'], step=0.10)

unabridged_threshold_input = st.slider("Pick a threshold for your unabridged top songs playlist", 
                                        min_value=0.0, max_value=17.0, value=slider_values['unabridged_threshold'], step=0.10)

# Save the new slider values when they are changed
save_slider_values(top_100_threshold_input, unabridged_threshold_input)

# Function to add a new song
def add_song(song_input, artist_input, date_added_input, is_chokehold_input, emotional_input, banger_input, is_iconic_input, is_listened_input, is_remembered_input, is_day6_input):
    if song_input.strip() == "" or artist_input.strip() == "":
        st.error("Both song title and artist title must be filled!")
        return

    date_added_str = date_added_input.strftime('%Y-%m-%d') if isinstance(date_added_input, datetime.date) else date_added_input

    # Calculate total score
    totalScore = calculate_total_score(date_added_input, is_chokehold_input, emotional_input, banger_input, is_iconic_input, is_listened_input)
    
    # Assign playlist
    playlist = playlist_assignment(totalScore, song_input, is_day6_input, top_100_threshold_input, unabridged_threshold_input)

    new_song = pd.DataFrame([{
        "Title": song_input,
        "Artist": artist_input,
        "Chokehold": int(is_chokehold_input),
        "Emotional": emotional_input,
        "Banger": banger_input,
        "Iconic": is_iconic_input,
        "StillListen": is_listened_input,
        "Remember": is_remembered_input,
        "DAY6": is_day6_input,
        "DateAdded": date_added_str,
        "TotalScore": totalScore,
        "Playlist": playlist        
    }])

    # Check for duplicates
    if ((st.session_state.data['Title'] == song_input) & (st.session_state.data['Artist'] == artist_input)).any():
        st.error("This song already exists.")
    else:
        st.session_state.data = pd.concat([st.session_state.data, new_song], ignore_index=True) 
        st.session_state.data.to_excel(path, index=False)
        st.success("Song added successfully!")

# Streamlit form for input
with st.form("Song Input Form"):
    song_input = st.text_input("Enter the song name", "")
    artist_input = st.text_input("Enter the artist name", "")
    date_added_input = st.date_input("Enter the date you added the song")
    emotional_input = st.number_input("How emotional or personal is this song to you?", min_value=0.0, max_value=5.0, value=0.0, step=0.5)
    banger_input = st.number_input("How much of a banger is this song?", min_value=0.0, max_value=5.0, value=0.0, step=0.5)
    is_chokehold_input = st.checkbox("Is it a chokehold song?")
    is_iconic_input = st.checkbox("Is it an iconic song?")
    is_listened_input = st.checkbox("Do you still listen to this song?")
    is_remembered_input = st.checkbox("Be honest: do you remember how this song goes?")
    is_day6_input = st.checkbox("Is this song by DAY6 and not from 2024?")

    add_song_button = st.form_submit_button("Add Song")

    if add_song_button:
        add_song(song_input, artist_input, date_added_input, is_chokehold_input, emotional_input, banger_input, is_iconic_input, is_listened_input, is_remembered_input, is_day6_input)

# Table to show current data
st.table(st.session_state.data)

# If the song input is defined, show the summary
if song_input and artist_input:
    totalScore = calculate_total_score(date_added_input, is_chokehold_input, emotional_input, banger_input, is_iconic_input, is_listened_input)
    playlist = playlist_assignment(totalScore, song_input, is_day6_input, top_100_threshold_input, unabridged_threshold_input)
    
    if totalScore and playlist:  # Check if both values are defined
        st.markdown(
            f"""
            * Song: {song_input} by {artist_input}
            * Date added: {date_added_input}
            * Emotional?: {emotional_input}
            * Banger: {banger_input}
            * Chokehold?: {is_chokehold_input}
            * Iconic?: {is_iconic_input}
            * Still Listen?: {is_listened_input}
            * Remember it?: {is_remembered_input}
            * Top Song Threshold: {top_100_threshold_input}
            * Unabridged Song Threshold: {unabridged_threshold_input}
            * Total Score: {totalScore}
            * Assigned Playlist: {playlist}
            """
        )