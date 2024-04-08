import streamlit as st
from annotated_text import annotated_text
import whisper
import assemblyai as aai
import tempfile
from transformers import pipeline
import requests
import os
import time as tm
from dotenv import load_dotenv
from src.utils import compare_texts
import jiwer

def show():
    
    st.header(":speech_balloon: Speech-2-Text")
    load_dotenv()

    transforms = jiwer.Compose(
        [
            jiwer.ExpandCommonEnglishContractions(),
            jiwer.RemoveEmptyStrings(),
            jiwer.ToLowerCase(),
            jiwer.RemoveMultipleSpaces(),
            jiwer.Strip(),
            jiwer.RemovePunctuation(),
            jiwer.ReduceToListOfListOfWords(),
        ]
    )

    def time_it(func):
        def wrapper(*args, **kwargs):
            start_time = tm.time()
            result = func(*args, **kwargs) 
            end_time = tm.time()
            execution_time = end_time - start_time 
            result['time'] = round(execution_time,2)
            return result
        return wrapper

    @time_it
    def transcribe_whisper(audio_path):
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, fp16=False)
        return {"text": result["text"]}
    
    @time_it
    def transcribe_wav2vec2(audio_path):
        API_TOKEN = os.getenv('wav2vec2_TOKEN')
        API_URL = "https://api-inference.huggingface.co/models/facebook/wav2vec2-large-xlsr-53-german"
        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        with open(audio_path, "rb") as f:
            data = f.read()

        result = requests.post(API_URL, headers=headers, data=data).json()
        return {"text": result["text"]}
    
    @time_it
    def transcribe_wav2vec2_tuned(audio_path):
        API_TOKEN = os.getenv('wav2vec2_TOKEN')
        API_URL = "https://api-inference.huggingface.co/models/jonatasgrosman/wav2vec2-large-xlsr-53-german"
        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        with open(audio_path, "rb") as f:
            data = f.read()

        result = requests.post(API_URL, headers=headers, data=data).json()
        return {"text": result["text"]}
    
    @time_it
    def transribe_assemblyAI(audio_path):
        API_TOKEN = os.getenv('assemblyAI_TOKEN')
        aai.settings.api_key = API_TOKEN
        config = aai.TranscriptionConfig(language_code="de")
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(audio_path)
        return {"text": transcript.text}

    # Initialize audio_path to None
    audio_path = None
    uploaded_file = None

    if st.session_state['selected_example']:
        uploaded_file = True

        audio_path = os.path.join("audio", st.session_state['selected_example'])
        text_path = os.path.join("text", st.session_state['selected_example'])
        audio_path = os.path.join("audio", f"{st.session_state['selected_example']}.wav")
        text_path = os.path.join("text", f"{st.session_state['selected_example']}.txt")

    if audio_path:
        st.audio(audio_path, format='audio/wav')


    if uploaded_file is not None:

        with open(text_path, 'r', encoding='utf-8') as file:
            original_text = file.read()

        col1, col2 = st.columns([5, 1])

        with col1:
            st.text_area("Original", value=original_text, height=200, key="original_text")

        with col2:
            st.write("")
            st.write('The highlighting of the errors doesnt take lower or upper cases into account. But it does look for missing "," & "." vaues.')
            st.write('The "Word Error Rate" is calculated for every model. It doesnt take "," & "." into account.')

        col1, col2 = st.columns(2)

        with col1:
            transcription_message_1 = st.empty()
            transcription_message_1.caption("Transcribing with Whisper Base...")
            transcription_whisper = transcribe_whisper(audio_path)
            #####
            time = transcription_whisper["time"]
            hypothesis = transcription_whisper["text"]
            wer = round(jiwer.wer(
                original_text,
                hypothesis,
                truth_transform=transforms,
                hypothesis_transform=transforms,
            ), 2)
            #####
            title = f"Whisper Base Transcription ({time}s / WER {wer})"
            transcription_message_1.caption(title)
            diff_text = compare_texts(original_text, hypothesis)
            annotated_text(*diff_text)

        with col2:
            transcription_message_2 = st.empty()
            transcription_message_2.text("Transcribing with Wav2Vec large german...")
            transcription_wav2vec = transcribe_wav2vec2(audio_path)
            #####
            time = transcription_wav2vec["time"]
            hypothesis = transcription_wav2vec["text"]
            wer = round(jiwer.wer(
                original_text,
                hypothesis,
                truth_transform=transforms,
                hypothesis_transform=transforms,
            ), 2)
            #####
            title = f"Wav2Vec large german Transcription ({time}s / WER {wer})"
            transcription_message_2.caption(title)
            diff_text = compare_texts(original_text, hypothesis)
            annotated_text(*diff_text)

        col1, col2 = st.columns(2)

        with col1:
            transcription_message_3 = st.empty()
            transcription_message_3.text("Transcribing with Wav2Vec large german (tuned)...")
            transcription_wav2vec_tuned = transcribe_wav2vec2_tuned(audio_path)
            #####
            time = transcription_wav2vec_tuned["time"]
            hypothesis = transcription_wav2vec_tuned["text"]
            wer = round(jiwer.wer(
                original_text,
                hypothesis,
                truth_transform=transforms,
                hypothesis_transform=transforms,
            ), 2)
            #####
            title = f"Wav2Vec large german Transcription tuned ({time}s / WER {wer})"
            transcription_message_3.caption(title)
            diff_text = compare_texts(original_text, hypothesis)
            annotated_text(*diff_text)

        with col2:
            transcription_message_4 = st.empty()
            transcription_message_4.text("Transcribing with AssemblyAI...")
            transcription_assemblyAI = transribe_assemblyAI(audio_path)
            #####
            time = transcription_assemblyAI["time"]
            hypothesis = transcription_assemblyAI["text"]
            wer = round(jiwer.wer(
                original_text,
                hypothesis,
                truth_transform=transforms,
                hypothesis_transform=transforms,
            ), 2)
            title = f"AssemblyAI Transcription ({time}s / WER {wer})"
            transcription_message_4.caption(title)
            diff_text = compare_texts(original_text, hypothesis)
            annotated_text(*diff_text)

