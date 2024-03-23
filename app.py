import streamlit as st
import whisper
import tempfile
from transformers import pipeline
import requests
import os
from dotenv import load_dotenv

def show():
    st.header(":gear: App")

    API_TOKEN = os.getenv('API_TOKEN')

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
    
    uploaded_file = st.file_uploader("Choose a WAV file", type=["wav"])

    # Initialize audio_path to None
    audio_path = None

    if uploaded_file is not None:
        # If a file was uploaded, use it
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            audio_path = tmp_file.name
    elif st.session_state['selected_example']:
        uploaded_file = True
        audio_path = os.path.join(st.session_state['example_audios_dir'], st.session_state['selected_example'])

    if audio_path:
        st.audio(audio_path, format='audio/wav')

    col1, col2 = st.columns(2)

    if uploaded_file is not None:

        if uploaded_file is True:
            audio_path = os.path.join(st.session_state['example_audios_dir'], st.session_state['selected_example'])
        
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