import streamlit as st
import os

from recording import show as show_recording
from insights import show as show_insights
from app import show as show_app

st.set_page_config(layout="wide")
st.session_state['example_audios_dir'] = "./audio"

with st.sidebar:
    st.image("./assets/structure.png")

    example_audio_files = [f for f in os.listdir(st.session_state['example_audios_dir']) if os.path.isfile(os.path.join(st.session_state['example_audios_dir'], f))]

    st.session_state['selected_example'] = st.selectbox(
        "Select an example Audio file",
        example_audio_files,
        index=None,
        format_func=lambda x: x if x != "Richard Example" else "Select an example audio file...",
    )

    if st.session_state['selected_example']:
        st.write('You selected:', st.session_state['selected_example'])
        example_audio_path = os.path.join(st.session_state['example_audios_dir'], st.session_state['selected_example'])

    gap_height = 200
    st.markdown(f"<div style='margin: {gap_height}px;'></div>", unsafe_allow_html=True)
    st.image("./assets/logo.png")

tab1, tab2, tab3 = st.tabs([":gear: App", ":loud_sound: Recording", ":blue_book: Insights"])

col1, col2 = st.columns(2)

with tab1:
    show_app()

with tab2:
    show_recording()

with tab3:
    show_insights()
    