import streamlit as st
import whisper
import tempfile
from pydub import AudioSegment
from st_audiorec import st_audiorec
from transformers import pipeline
import requests
import os

API_TOKEN = "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"

def transcribe_facebook(audio_path):
    url = "https://api-inference.huggingface.co/models/facebook/wav2vec2-large-xlsr-53-german"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    with open(audio_path, "rb") as f:
        data = f.read()
    response = requests.request("POST", url, headers=headers, data=data)
    json_response = response.json()
    return json_response['text']

def transcribe_whisper(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, fp16=False)
    return result["text"]

st.set_page_config(layout="wide")



with st.sidebar:
    st.image("./assets/structure.png")

    example_audios_dir = "./audio"
    example_audio_files = [f for f in os.listdir(example_audios_dir) if os.path.isfile(os.path.join(example_audios_dir, f))]

    selected_example = st.selectbox(
        "Select an example Audio file",
        example_audio_files,
        index=None,
        format_func=lambda x: x if x != "Richard Example" else "Select an example audio file...",
    )

    if selected_example:
        st.write('You selected:', selected_example)
        example_audio_path = os.path.join(example_audios_dir, selected_example)

    gap_height = 200
    st.markdown(f"<div style='margin: {gap_height}px;'></div>", unsafe_allow_html=True)
    st.image("./assets/logo.png")

tab1, tab2, tab3 = st.tabs([":gear: Main", ":loud_sound: Recording", ":blue_book: Insights"])

col1, col2 = st.columns(2)

with tab1:

    uploaded_file = st.file_uploader("Choose a WAV file", type=["wav"])

    # Initialize audio_path to None
    audio_path = None

    if uploaded_file is not None:
        # If a file was uploaded, use it
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            audio_path = tmp_file.name
    elif selected_example:
        uploaded_file = True

    if audio_path:
        st.audio(audio_path, format='audio/wav')

    col1, col2 = st.columns(2)

    if uploaded_file is not None:

        if uploaded_file is True:
            audio_path = os.path.join(example_audios_dir, selected_example)
        
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                audio_path = tmp_file.name

        with col1:
            transcription_message_1 = st.empty()
            transcription_message_1.text("Transcribing with Whisper...")
            transcription_whisper = transcribe_whisper(audio_path)
            st.text_area("Whisper Transcription", value=transcription_whisper, height=200, key="whisper")
            transcription_message_1.empty()

        with col2:
            transcription_message_2 = st.empty()
            transcription_message_2.text("Transcribing with Wav2Vec 2.0 - German...")
            transcription_wav2vec = transcribe_facebook(audio_path)
            st.text_area("Wav2Vec 2.0 - German Transcription", value=transcription_wav2vec, height=200, key="wav2vec")
            transcription_message_2.empty()

        def correct_output(text):
            fix_spelling = pipeline("text2text-generation",model="oliverguhr/spelling-correction-german-base")
            return fix_spelling(text, max_length=256)

        with col1:
            transcription_message_3 = st.empty()
            transcription_message_3.text("Checking with spelling-correction-german-base ...")
            corrected_whisper = correct_output(transcription_whisper)
            st.text_area("Corrected Whisper Transcription", value=corrected_whisper[0]['generated_text'], height=200, key="corr_whisper")
            transcription_message_3.empty()
        with col2:
            transcription_message_4 = st.empty()
            transcription_message_4.text("Checking with spelling-correction-german-base ...")
            corrected_wav2vec = correct_output(transcription_wav2vec)
            st.text_area("Corrected Wav2Vec 2.0 - German", value=corrected_wav2vec[0]['generated_text'], height=200, key="corr_wav2vec")
            transcription_message_4.empty()

with tab2:
    recorded_audio = st_audiorec()

    # Function to convert audio to WAV format
    def convert_audio_to_wav(audio_file):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            sound = AudioSegment.from_file(audio_file)
            sound = sound.set_channels(1).set_frame_rate(16000)
            sound.export(tmp_file.name, format="wav")
            return tmp_file.name

    if recorded_audio is not None:
        # Assuming recorded_audio is a bytes-like object; adjust as necessary based on st_audiorec's output
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(recorded_audio.getvalue())
            audio_path = tmp_file.name
        st.audio(audio_path, format='audio/wav')