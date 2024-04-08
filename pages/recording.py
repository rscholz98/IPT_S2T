import streamlit as st
from st_audiorec import st_audiorec
import os
import datetime

def show():
    st.header(":loud_sound: Recording")
    
    recorded_audio = st_audiorec()

    audio_dir = "../audio"
    os.makedirs(audio_dir, exist_ok=True)  # Ensure the directory exists

    # Function to save audio to WAV format in the specified directory
    def save_audio_to_wav(audio_bytes, directory):
        file_path = os.path.join(directory, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".wav")
        with open(file_path, "wb") as f_out:
            f_out.write(audio_bytes.getvalue())
        return file_path

    if recorded_audio is not None:
        audio_path = save_audio_to_wav(recorded_audio, audio_dir)
        st.audio(audio_path, format='audio/wav')

    # Display the list of audio files in the directory
    st.header("Recorded Audio Files")
    for filename in os.listdir(audio_dir):
        file_path = os.path.join(audio_dir, filename)
        creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"{filename} (created: {creation_time})")
