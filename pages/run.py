import streamlit as st
import whisper
import tempfile
from transformers import pipeline
import requests
import os
from dotenv import load_dotenv

def show():
    st.header(":gear: App")

    