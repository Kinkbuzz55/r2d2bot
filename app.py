import streamlit as st
from groq import Groq
from gtts import gTTS
import base64
import os
import re

# 1. Matrix Theme UI
st.set_page_config(page_title="Matrix AI", page_icon="🤖", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; color: #00ff41; }
    audio { display: none; }
    </style>
    """, unsafe_allow_html=True)

# API Key Check
if "GROQ_API_KEY" not in st.secrets:
    st.error("Bhai, Streamlit Secrets mein 'GROQ_API_KEY' set karein!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 2. Voice Function
def matrix_speak(text):
    clean_text = re.sub(r'[^\w\s,.?]', '', text)
    tts = gTTS(text=clean_text, lang='hi', slow=False)
    tts.save("voice.mp3")
    with open("voice.mp3", "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay></audio>', unsafe_allow_html=True)

# 3. UI & Chat
st.title("🤖 Matrix: Voice & Vision")
voice_input = st.audio_input("🎤 Bol kar puchiye")
text_input = st.chat_input("⌨️ Type karein")

user_query = None
should_speak = False

if voice_input:
    with st.spinner("Matrix sun raha hai..."):
        transcription = client.audio.transcriptions.create(
            file=("audio.wav", voice_input.read()),
            model="whisper-large-v3"
        )
        user_query = transcription.text
        should_speak = True

if text_input:
    user_query = text_input
    should_speak = False

if user_query:
    st.chat_message("user").write(user_query)
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[{"role": "user", "content": user_query}],
            max_tokens=500
        )
        reply = response.choices[0].message.content
        st.write(reply)
        if should_speak:
            matrix_speak(reply)