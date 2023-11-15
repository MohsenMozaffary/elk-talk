import streamlit as st
import tkinter as tk
from tkinter import filedialog
import os
from main_UI import process_main
from pydub import AudioSegment
from pydub.playback import play


def browse_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()  # Close the Tkinter window explicitly
    return file_path

def play_audio(audio_path):
    sound = AudioSegment.from_file(audio_path)
    play(sound)



# Set page configuration for responsiveness
st.set_page_config(
    page_title="ELK_talk",
    page_icon="🧙",
    layout="wide",  # "wide" layout adapts to different screen sizes
    initial_sidebar_state="collapsed"
)


# Title
st.title("Welcome to ELK talk app!")

# Sidebar and main content layout
with st.container():
    # Sidebar
    st.sidebar.header('Specification')
    st.sidebar.markdown("&nbsp;")

    if 'file_path' not in st.session_state:
        st.session_state.file_path = "abc"

    # Help message for number of repeats
    st.sidebar.markdown("**Number of Repeats:** Specify how many times the audio should be repeated.")
    n_repeats = int(st.sidebar.text_input(' ', value="1"))
    st.session_state.n_repeats = n_repeats
    st.sidebar.markdown("&nbsp;")

    # Help message for silence duration
    st.sidebar.markdown("**Silence Duration:** Specify the duration of silence between repeated audio.")
    silence_duration = int(st.sidebar.text_input('', value="1"))
    st.session_state.silence_duration = silence_duration
    st.sidebar.markdown("&nbsp;")

    # Help message for volume adjustment
    st.sidebar.markdown("**Adjust Volume:** Use the slider to adjust the volume of the audio.")
    vol = float(st.sidebar.slider('   ', 0.0, 1.0, 0.5, 0.01))
    st.session_state.vol = vol
    st.sidebar.markdown("&nbsp;")

    # Browse files button
    if st.sidebar.button("Browse files"):
        with st.spinner("Loading file..."):
            file_path = browse_file()
            st.session_state.file_path = file_path
            st.success("File successfully loaded!")

# Create files button and result display
col1, col2 = st.columns([2, 1])  # Use columns for a responsive layout

with col1:
    # Create files button
    if st.button("Generate audio files"):
        if not hasattr(st.session_state, 'file_path') or not os.path.exists(st.session_state.file_path):
            st.warning("Please browse and select a valid file before creating files.")
        else:
            with st.spinner("Creating files..."):
                eaf_location = os.path.dirname(st.session_state.file_path)
                sound_dir = eaf_location
                saving_dir = os.path.join(sound_dir, "results")
                st.session_state.saving_dir = saving_dir

                if not os.path.exists(saving_dir):
                    os.mkdir(saving_dir)

                process_main(st.session_state.file_path, saving_dir, sound_dir, vol=st.session_state.vol,
                             n_repeats=st.session_state.n_repeats, silence_duration=st.session_state.silence_duration,
                             title="translation")
                st.success("Files successfully created!")

with col2:
    # Display selected file
    try:
        sound_files = [file for file in os.listdir(st.session_state.saving_dir) if file.endswith((".mp3", ".wav"))]
        selected_file = st.selectbox("Select a sound file", sound_files)
        selected_file_path = os.path.join(st.session_state.saving_dir, selected_file)
        st.audio(selected_file_path, format='audio/wav', start_time=0)
    except:
        pass
