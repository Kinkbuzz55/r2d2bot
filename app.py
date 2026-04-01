import streamlit as st
from groq import Groq
import base64

# 1. Page Configuration
st.set_page_config(page_title="Matrix AI", page_icon="🤖", layout="wide")
st.title("🤖 Matrix AI: Syed Aves Edition")
st.markdown("---")

# 2. Connection to Groq (Using Secrets)
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Please add GROQ_API_KEY in Streamlit Secrets!")
    st.stop()

# 3. IDENTITY LOCK (Syed Aves Name + Emojis)
system_prompt = (
    "You are Matrix AI, a high-end assistant created by Syed Aves. "
    "Introduce yourself as 'Syed Aves's Matrix AI' at the start of every chat. "
    "Always use plenty of emojis (🚀, 🦾, ✨) and professional Hinglish. 🦾"
)

# 4. IMAGE UPLOAD SECTION (Sidebar)
with st.sidebar:
    st.header("Matrix Settings")
    uploaded_file = st.file_uploader("🖼️ Photo upload karein", type=["jpg", "png", "jpeg"])
    if st.button("Clear Chat 🗑️"):
        st.session_state.messages = []
        st.rerun()

# 5. Chat History Management
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. User Input & Logic
user_query = st.chat_input("Syed Aves, main aapki kya madad kar sakta hoon?")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    messages = [{"role": "system", "content": system_prompt}]
    
    if uploaded_file:
        image_data = base64.b64encode(uploaded_file.read()).decode("utf-8")
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": user_query},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]
        })
        model_id = "llama-3.2-11b-vision-preview" 
    else:
        messages.append({"role": "user", "content": user_query})
        model_id = "llama-3.3-70b-versatile"

    # Final Response Generation
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(model=model_id, messages=messages)
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error: {e}")