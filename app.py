import streamlit as st
from groq import Groq
import base64

# 1. Page Configuration (Centered for Mobile & Clean UI)
st.set_page_config(page_title="Matrix AI", page_icon="🦾", layout="centered")

# CSS: Professional Mobile ChatGPT Look
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stChatInput { border-radius: 25px; }
    /* Mobile optimization */
    [data-testid="stFileUploader"] { padding: 0; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦾 Matrix")
st.caption("Created by Syed Aves | 2026 Multi-Modal Engine")
st.markdown("---")

# 2. Connection to Groq (2026 API)
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Bhai, Streamlit Secrets mein GROQ_API_KEY missing hai!")
    st.stop()

# 3. THE "MATRIX" CORE (Identity, Language & Emoji Lock)
system_prompt = (
    "Identity: Your name is 'Matrix'. You are a super-intelligent AI created by Syed Aves. "
    "MANDATORY RULES:\n"
    "1. NAME: Always identify as 'Matrix'. NEVER say your name is 'Syed AvesMatrix'.\n"
    "2. CREATOR: If asked who made you, reply 'I was created by Syed Aves'.\n"
    "3. EMOJIS: Use 3-4 emojis in EVERY sentence (🚀, 🦾, ✨, 🔥, 🤖). Use them aggressively! ✨🦾\n"
    "4. LANGUAGE: Speak English, Hindi, or Hinglish based on the user. No 'Shuddh' (formal) Hindi. "
    "Use natural Hinglish (e.g., 'Bhai, main help kar sakta hoon').\n"
    "5. INTELLIGENCE: Be professional and highly accurate. No spelling mistakes."
)

# 4. CHAT HISTORY MANAGEMENT
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. INPUT UI (ChatGPT Style Layout)
# Voice aur Image buttons ko chat bar ke thik upar rakha hai
col1, col2 = st.columns([1, 1])
with col1:
    uploaded_file = st.file_uploader("🖼️ Image (Vision)", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
with col2:
    recorded_audio = st.audio_input("🎤 Voice", label_visibility="collapsed")

# Main Text Input (Acts as the 'SEND' button for everything)
user_query = st.chat_input("Ask Matrix... (Select Image/Voice and press Enter 🚀)")

# 6. PROCESSING LOGIC
# Voice Transcription (Whisper v3 Turbo)
if recorded_audio:
    with st.spinner("Matrix sun raha hai... 🎤"):
        try:
            transcription = client.audio.transcriptions.create(file=recorded_audio, model="whisper-large-v3-turbo")
            user_query = transcription.text
        except Exception as e: st.error(f"Voice Error: {e}")

# TRIGGER: Jab user 'Enter' dabaye ya click kare
if user_query or uploaded_file:
    # Default text agar user ne sirf image bheji ho
    final_query = user_query if user_query else "Describe this image in detail 🚀"
    
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"):
        st.markdown(final_query)

    messages = [{"role": "system", "content": system_prompt}]
    
    # 2026 Vision Logic (Replacing decommissioned Llama 3.2)
    if uploaded_file:
        image_data = base64.b64encode(uploaded_file.read()).decode("utf-8")
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": final_query},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]
        })
        # Llama 4 Scout is the current recommended vision model [35, 16]
        model_id = "meta-llama/llama-4-scout-17b-16e-instruct" 
    else:
        # High Knowledge Text Model
        messages.append({"role": "user", "content": final_query})
        model_id = "llama-3.3-70b-versatile"

    # AI Response Generation
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(model=model_id, messages=messages)
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Matrix Error: {e}")