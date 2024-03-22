import streamlit as st
import whisper
import tempfile
from pydub import AudioSegment
from st_audiorec import st_audiorec

# Function to convert audio to WAV format
def convert_audio_to_wav(audio_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        sound = AudioSegment.from_file(audio_file)
        sound = sound.set_channels(1).set_frame_rate(16000)
        sound.export(tmp_file.name, format="wav")
        return tmp_file.name

# Function to transcribe audio
def transcribe_audio(audio_path):
    model = whisper.load_model("base")  # Consider using a different model size based on your needs
    result = model.transcribe(audio_path, fp16=False)
    return result["text"]

st.set_page_config(layout="wide")
st.title(":loud_sound: Sprach Pro :loud_sound:")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Choose a WAV file",type=["wav"])

with col2:
    wav_audio_data = st_audiorec()
    if wav_audio_data is not None:
        st.audio(wav_audio_data, format='audio/wav')

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        audio_path = tmp_file.name

    # Transcribe and display
    st.write("Transcribing...")
    transcription = transcribe_audio(audio_path)
    st.text_area("Transcription", value=transcription, height=200)