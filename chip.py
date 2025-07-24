import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# 🔐 Set your Gemini API key
genai.configure(api_key="AIzaSyAa7SQGBixtGVAKgI72tGqtMUkJJs5AUAw")  # Replace with your real key

# ✅ Use a fast and supported Gemini model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
chat = model.start_chat(history=[])

# 🌐 Streamlit UI
st.set_page_config(page_title="💡 Chip Design Chatbot", layout="centered")

# Ensure chat history is initialized before any access
if "messages" not in st.session_state:
    st.session_state.messages = []

# Persistent chat history file
history_file = 'chat_history.json'

# Load history at startup
if "messages" not in st.session_state:
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            st.session_state.messages = json.load(f)
    else:
        st.session_state.messages = []

def save_history():
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.messages, f)

# ---------- Custom CSS Styling ----------
page_bg_img = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027 0%, #2c5364 100%, #00f0ff 100%);
    min-height: 100vh;
    position: relative;
    font-family: 'Montserrat', sans-serif;
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 0, 0, 0.45);
    z-index: 0;
}

.header-img {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-top: 48px;
    margin-bottom: 0px;
    z-index: 2;
    background: rgba(20, 20, 30, 0.98);
    border: 2.5px solid #fff;
    border-radius: 32px;
    box-shadow: 0 6px 32px #000a, 0 0 0 4px #00f0ff55;
    padding: 32px 32px 18px 32px;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}
.header-img .header-icons {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 18px;
    margin-bottom: 8px;
}
.header-img .header-emoji {
    background: #fff;
    border-radius: 50%;
    box-shadow: 0 2px 12px #0003;
    padding: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 38px;
}
.header-img img {
    width: 54px;
    height: 54px;
    border-radius: 50%;
    background: #fff;
    box-shadow: 0 2px 16px #0003;
    padding: 6px;
}
h1 {
    text-align: center;
    font-size: 62px;
    color: #00f0ff;
    font-weight: 900;
    font-family: 'Montserrat', sans-serif;
    margin-bottom: 18px;
    margin-top: 0;
    position: relative;
    z-index: 3;
    padding: 0 0 0 0;
    border-radius: 0;
    background: linear-gradient(90deg, #00f0ff 0%, #007cf0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-fill-color: transparent;
    text-shadow: 2px 2px 12px #000, 0 4px 24px #000a;
    display: inline-block;
    margin-left: auto;
    margin-right: auto;
}

.input-row {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
}
.input-row .stTextInput > div > div > input {
    background: rgba(255,255,255,0.18);
    border: 1.5px solid #00f0ff;
    border-radius: 10px;
    color: #fff;
    font-size: 18px;
    font-family: 'Montserrat', monospace;
    padding: 10px 16px;
    margin-bottom: 0;
    transition: box-shadow 0.3s;
    z-index: 1;
}
.input-row .stTextInput > div > div > input:focus {
    box-shadow: 0 0 0 2px #00f0ff44;
    outline: none;
}
.input-row .stButton > button {
    background: linear-gradient(90deg, #00f0ff 0%, #00ffcc 100%);
    color: #222;
    border: none;
    border-radius: 10px;
    font-size: 18px;
    font-weight: bold;
    font-family: 'Montserrat', sans-serif;
    padding: 10px 30px;
    margin-top: 0;
    margin-bottom: 0;
    box-shadow: 0 2px 8px #00f0ff33;
    transition: background 0.3s, transform 0.2s;
    cursor: pointer;
    z-index: 1;
}
.input-row .stButton > button:hover {
    background: linear-gradient(90deg, #00ffcc 0%, #00f0ff 100%);
    transform: translateY(-2px) scale(1.03);
}

.chat-area {
    width: 100%;
    max-width: 900px;
    margin: 0 auto 0 auto;
    overflow-y: auto;
    max-height: 60vh;
    padding-right: 8px;
    scrollbar-width: thin;
    scrollbar-color: #00f0ff #222;
    border-radius: 20px;
    border: 2.5px solid #00f0ff;
    box-shadow: 0 0 24px #00f0ff55;
    background: rgba(0,0,0,0.18);
    backdrop-filter: blur(2px);
    z-index: 1;
}

.chatbox {
    background: rgba(0, 0, 0, 0.45);
    border-radius: 18px;
    padding: 18px 22px;
    margin: 14px auto;
    max-width: 800px;
    color: #fff;
    font-size: 17px;
    font-family: 'Montserrat', monospace;
    box-shadow: 0 4px 32px #00f0ff22;
    backdrop-filter: blur(7px);
    border: 1.5px solid #00f0ff33;
    animation: fadeIn 0.7s;
    position: relative;
    z-index: 1;
}

.user-msg {
    color: #00ffcc;
    text-align: right;
    font-weight: 600;
    background: linear-gradient(90deg, #00f0ff33 0%, #00ffcc22 100%);
    border-right: 4px solid #00ffcc;
    border-left: none;
    margin-left: 80px;
    margin-right: 0;
}

.bot-msg {
    color: #ffd700;
    text-align: left;
    font-weight: 500;
    background: linear-gradient(90deg, #222 0%, #00f0ff22 100%);
    border-left: 4px solid #ffd700;
    border-right: none;
    margin-right: 80px;
    margin-left: 0;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.footer {
    text-align: center;
    color: #00f0ff;
    font-size: 18px;
    margin-top: 30px;
    font-family: 'Montserrat', sans-serif;
    opacity: 0.85;
    z-index: 1;
    margin-bottom: 40px;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ---------- UI Title ----------
st.markdown('<div class="header-img">'
            '<div class="header-icons">'
            '<span class="header-emoji">🤖</span>'
            '<img src="https://cdn-icons-png.flaticon.com/512/2869/2869676.png" alt="chip"/>'
            '<span class="header-emoji">🔩</span>'
            '</div>'
            '<h1>Chip Design Chatbot <span style="font-size:0.7em;">✨</span></h1>'
            '</div>', unsafe_allow_html=True)

# ---------- Sidebar for Previous Chat ----------
CHAT_DIR = "chats"
os.makedirs(CHAT_DIR, exist_ok=True)

def list_chat_files():
    return sorted([f for f in os.listdir(CHAT_DIR) if f.endswith('.json')], reverse=True)

def save_current_chat():
    if st.session_state.messages:
        # Use the first user message and timestamp for filename
        first_msg = st.session_state.messages[0]['content'][:20].replace(' ', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"chat_{timestamp}_{first_msg}.json"
        with open(os.path.join(CHAT_DIR, filename), 'w', encoding='utf-8') as f:
            json.dump(st.session_state.messages, f)

def load_chat(filename):
    with open(os.path.join(CHAT_DIR, filename), 'r', encoding='utf-8') as f:
        st.session_state.messages = json.load(f)
    st.rerun()

# Sidebar: List all chats and New Chat button
with st.sidebar:
    st.title('💬 Chat History')
    if st.button('➕ New Chat'):
        st.session_state.messages = []
        st.rerun()
    latest_per_topic = {}
    for chat_file in list_chat_files():
        parts = chat_file.replace('.json', '').split('_')
        if len(parts) >= 4:
            topic = ' '.join(parts[3:]).replace('_', ' ')
            latest_per_topic[topic] = chat_file  # This will keep the last (most recent) file for each topic

    for topic, chat_file in latest_per_topic.items():
        parts = chat_file.replace('.json', '').split('_')
        time_str = parts[2][0:2] + ':' + parts[2][2:4]  # HH:MM
        label = f"{time_str} {topic}"
        if st.button(label, key=chat_file):
            load_chat(chat_file)

# ---------- Input Row Just Below Header ----------
st.markdown('<div class="input-row">', unsafe_allow_html=True)
user_input = st.chat_input("Ask your chip design question here...")
# Remove the button from the main input row (if present)
st.markdown('</div>', unsafe_allow_html=True)

# User input logic and Gemini response (handle before rendering chat area)
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    save_current_chat()
    try:
        response = chat.send_message(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        save_current_chat()
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ---------- Chat Area Below Input ----------
msgs = st.session_state.messages
# Only show chat area if there is at least one complete user+assistant pair
pairs = []
i = 0
while i < len(msgs) - 1:
    if msgs[i]["role"] == "user" and msgs[i+1]["role"] == "assistant" and msgs[i+1]["content"].strip():
        pairs.append((msgs[i]["content"].strip(), msgs[i+1]["content"].strip()))
        i += 2
    else:
        i += 1
if pairs:
    st.markdown('<div class="chat-area">', unsafe_allow_html=True)
    for user_msg, bot_msg in pairs:
        if user_msg:
            st.markdown(f"<div class='chatbox user-msg'>🧑‍💻 <span style='font-size:1.3em;'>🙋‍♂️</span> You: {user_msg}</div>", unsafe_allow_html=True)
        if bot_msg:
            st.markdown(f"<div class='chatbox bot-msg'>🤖 <span style='font-size:1.3em;'>💡</span> ChipGenie: {bot_msg}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown('<div class="footer">Made with ❤️ by Nida Saeed &nbsp;|&nbsp; <span style="font-size:1.2em;">🔬🪐</span></div>', unsafe_allow_html=True)
