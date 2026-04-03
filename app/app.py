import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import speech_recognition as sr
from datetime import datetime
from src.chatbot import get_response
from src.memory import save_chat

st.set_page_config(
    page_title="Support AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
#  ADVANCED MINIMALIST STYLES (BRIGHT MODE)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Base & Variables ── */
:root {
    --bg-main: #FAFAFA;
    --text-dark: #111827;
    --text-muted: #6B7280;
    --accent-blue: #2563EB;
    --accent-dark: #0F172A;
    --border-light: #E5E7EB;
    --white: #FFFFFF;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-float: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: var(--bg-main) !important;
    font-family: 'Inter', sans-serif;
    color: var(--text-dark);
}

/* Hide Streamlit Elements */
#MainMenu, header, footer, .stDeployButton, .viewerBadge_container__1QSob, div[data-testid="stToolbar"] { 
    display: none !important; 
}

/* ── Container ── */
.block-container {
    max-width: 720px !important;
    padding: 0 1rem 3rem !important;
    margin: 0 auto !important;
}

/* ── Modern Header ── */
.cs-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2rem 0 1.5rem;
    background: transparent;
    border-bottom: 1px solid var(--border-light);
    margin-bottom: 1.5rem;
}
.cs-logo {
    display: flex;
    align-items: center;
    gap: 12px;
}
.cs-logo-icon {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #0F172A, #334155);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    color: var(--white);
    box-shadow: var(--shadow-sm);
}
.cs-logo-text {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-dark);
    letter-spacing: -0.02em;
}
.cs-logo-sub {
    font-size: 12px;
    color: var(--text-muted);
    font-weight: 500;
}
.cs-status {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 500;
    color: var(--text-dark);
    background: var(--white);
    padding: 6px 12px;
    border-radius: 20px;
    border: 1px solid var(--border-light);
    box-shadow: var(--shadow-sm);
}
.cs-status-dot {
    width: 8px; height: 8px;
    background: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
    70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
    100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* ── Chat Area ── */
.cs-chat-area {
    display: flex;
    flex-direction: column;
    gap: 16px;
    min-height: 480px;
    max-height: 65vh;
    overflow-y: auto;
    padding: 10px 4px 20px;
    scrollbar-width: thin;
    scrollbar-color: #D1D5DB transparent;
}
.cs-chat-area::-webkit-scrollbar { width: 5px; }
.cs-chat-area::-webkit-scrollbar-thumb { background: #D1D5DB; border-radius: 10px; }

/* ── Bubbles & Animations ── */
.cs-row {
    display: flex;
    align-items: flex-end;
    gap: 12px;
    animation: springUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1) forwards;
    opacity: 0;
    transform: translateY(15px);
    width: 100%;
}
@keyframes springUp {
    to { opacity: 1; transform: translateY(0); }
}
.cs-row.user { 
    flex-direction: row-reverse; 
}

/* FIX: New wrapper to prevent flex squishing */
.cs-message-content {
    display: flex;
    flex-direction: column;
    max-width: 75%;
}
.cs-row.bot .cs-message-content {
    align-items: flex-start;
}
.cs-row.user .cs-message-content {
    align-items: flex-end;
}

.cs-avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px;
    font-weight: 600;
    flex-shrink: 0;
    box-shadow: var(--shadow-sm);
}
.cs-avatar.bot { background: var(--white); color: var(--accent-dark); border: 1px solid var(--border-light); }
.cs-avatar.user { background: var(--accent-dark); color: var(--white); }

.cs-bubble {
    padding: 12px 16px;
    border-radius: 20px;
    font-size: 15px;
    line-height: 1.5;
    box-shadow: var(--shadow-sm);
    width: fit-content;
    word-break: break-word;
    white-space: pre-wrap;
}
.cs-bubble.bot {
    background: var(--white);
    border: 1px solid var(--border-light);
    border-bottom-left-radius: 4px;
    color: var(--text-dark);
}
.cs-bubble.user {
    background: var(--accent-dark);
    color: var(--white);
    border-bottom-right-radius: 4px;
}
.cs-ts {
    font-size: 11px;
    color: #9CA3AF;
    margin-top: 4px;
    padding: 0 4px;
    font-weight: 500;
}
.cs-row.user .cs-ts { text-align: right; }

/* ── Empty State ── */
.cs-empty {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 3rem 0 2rem;
}
.cs-empty-icon { 
    font-size: 40px; 
    background: -webkit-linear-gradient(135deg, #0F172A, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.cs-empty-title { font-size: 20px; font-weight: 700; color: var(--text-dark); }
.cs-empty-sub   { font-size: 14px; color: var(--text-muted); text-align: center; }

/* ── Streamlit Buttons Restyling (For Suggestion Chips) ── */
.stButton > button {
    border-radius: 99px !important;
    border: 1px solid var(--border-light) !important;
    background: var(--white) !important;
    color: var(--text-dark) !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    padding: 8px 16px !important;
    height: auto !important;
    box-shadow: var(--shadow-sm) !important;
}
.stButton > button:hover {
    border-color: var(--accent-blue) !important;
    color: var(--accent-blue) !important;
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-md) !important;
}

/* ── Floating Input Bar ── */
.cs-input-wrap {
    position: relative;
    margin-top: 1.5rem;
    background: var(--white);
    border: 1px solid var(--border-light);
    border-radius: 30px;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 8px 6px 20px;
    box-shadow: var(--shadow-float);
    transition: all 0.3s ease;
}
.cs-input-wrap:focus-within {
    border-color: var(--accent-blue);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1), var(--shadow-float);
}

/* Override Streamlit text_input */
div[data-testid="stTextInput"] { flex: 1; min-width: 0; }
div[data-testid="stTextInput"] > div { background: transparent !important; border: none !important; }
div[data-testid="stTextInput"] input {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: var(--text-dark) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    padding: 8px 0 !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #9CA3AF !important; }

/* ── Input Bar Icon Buttons (Mic & Send) ── */
div[data-testid="column"]:nth-child(2) .stButton > button,
div[data-testid="column"]:nth-child(3) .stButton > button {
    border-radius: 50% !important;
    width: 42px !important; 
    height: 42px !important;
    padding: 0 !important;
    display: flex; align-items: center; justify-content: center !important;
}
/* Send button specific styling */
div[data-testid="column"]:nth-child(3) .stButton > button {
    background: var(--accent-dark) !important;
    color: var(--white) !important;
    border: none !important;
}
div[data-testid="column"]:nth-child(3) .stButton > button:hover {
    background: #1E293B !important;
    color: var(--white) !important;
    transform: scale(1.05) !important;
}

/* ── Listening Indicator ── */
.cs-listening {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 12px;
    background: rgba(37, 99, 235, 0.05);
    border: 1px solid rgba(37, 99, 235, 0.2);
    border-radius: 16px;
    font-size: 14px;
    font-weight: 500;
    color: var(--accent-blue);
    margin: 10px 0;
    animation: springUp 0.3s ease;
}
.cs-listening-dot span {
    display: inline-block;
    width: 6px; height: 6px;
    background: var(--accent-blue);
    border-radius: 50%;
    margin: 0 2px;
    animation: bounce 1.4s infinite ease-in-out both;
}
.cs-listening-dot span:nth-child(1) { animation-delay: -0.32s; }
.cs-listening-dot span:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
}

/* ── Footer ── */
.cs-footer {
    text-align: center;
    font-size: 12px;
    color: var(--text-muted);
    padding: 1.5rem 0 0;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "chat" not in st.session_state:
    st.session_state.chat = []
if "listening" not in st.session_state:
    st.session_state.listening = False
if "prefill" not in st.session_state:
    st.session_state.prefill = ""

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="cs-header">
  <div class="cs-logo">
    <div class="cs-logo-icon">✨</div>
    <div>
      <div class="cs-logo-text">Support AI</div>
      <div class="cs-logo-sub">Intelligent Assistant</div>
    </div>
  </div>
  <div class="cs-status">
    <div class="cs-status-dot"></div>
    Online
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  QUICK SUGGESTIONS (only when chat is empty)
# ─────────────────────────────────────────────
if not st.session_state.chat:
    st.markdown("""
    <div class="cs-empty">
      <div class="cs-empty-icon">✨</div>
      <div class="cs-empty-title">How can I help you today?</div>
      <div class="cs-empty-sub">Ask me anything — I'm here to assist you 24/7.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Track my order", use_container_width=True): st.session_state.prefill = "Track my order"
        if st.button("Change my password", use_container_width=True): st.session_state.prefill = "Change my password"
    with col2:
        if st.button("Return & refund policy", use_container_width=True): st.session_state.prefill = "Return & refund policy"
        if st.button("Billing issue", use_container_width=True): st.session_state.prefill = "Billing issue"

# ─────────────────────────────────────────────
#  CHAT MESSAGES
# ─────────────────────────────────────────────
if st.session_state.chat:
    chat_html = '<div class="cs-chat-area">'
    for i, (role, msg, ts) in enumerate(st.session_state.chat):
        delay = min(i * 0.05, 0.5) 
        avatar = "✨" if role == "bot" else "U"
        css = "bot" if role == "bot" else "user"
        
        # FIX: The bubble is now correctly wrapped inside .cs-message-content
        chat_html += f"""
        <div class="cs-row {css}" style="animation-delay: {delay}s;">
          <div class="cs-avatar {css}">{avatar}</div>
          <div class="cs-message-content">
            <div class="cs-bubble {css}">{msg}</div>
            <div class="cs-ts">{ts}</div>
          </div>
        </div>"""
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LISTENING INDICATOR
# ─────────────────────────────────────────────
if st.session_state.listening:
    st.markdown("""
    <div class="cs-listening">
      <div class="cs-listening-dot">
        <span></span><span></span><span></span>
      </div>
      Listening... Speak clearly.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  VOICE INPUT LOGIC
# ─────────────────────────────────────────────
def do_voice_input():
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.pause_threshold = 0.8
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.4)
            audio = r.listen(source, timeout=8, phrase_time_limit=12)
        return r.recognize_google(audio)
    except Exception:
        return ""

# ─────────────────────────────────────────────
#  GLASSMORPHISM INPUT BAR
# ─────────────────────────────────────────────
st.markdown('<div class="cs-input-wrap">', unsafe_allow_html=True)

col_text, col_mic, col_send = st.columns([8, 1, 1])

with col_text:
    default_val = st.session_state.prefill
    user_input = st.text_input(
        "message",
        value=default_val,
        placeholder="Type a message...",
        label_visibility="collapsed",
        key="msg_input"
    )
    if st.session_state.prefill:
        st.session_state.prefill = ""

with col_mic:
    if st.button("🎙️", key="mic_btn", help="Voice input"):
        st.session_state.listening = True
        st.rerun()

with col_send:
    send_clicked = st.button("↑", key="send_btn", help="Send message")

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HANDLE VOICE
# ─────────────────────────────────────────────
if st.session_state.listening:
    spoken = do_voice_input()
    st.session_state.listening = False
    if spoken:
        st.session_state.prefill = spoken
    st.rerun()

# ─────────────────────────────────────────────
#  SEND MESSAGE LOGIC
# ─────────────────────────────────────────────
def send_message(text: str):
    text = text.strip()
    if not text: return
    ts = datetime.now().strftime("%H:%M")
    
    with st.spinner(""):
        response = get_response(text)
        
    save_chat("User1", text, response)
    st.session_state.chat.append(("user", text, ts))
    bot_ts = datetime.now().strftime("%H:%M")
    st.session_state.chat.append(("bot", response, bot_ts))
    st.rerun()

if send_clicked and user_input:
    send_message(user_input)
elif user_input and user_input != default_val:
    pass 
if user_input and send_clicked:
    send_message(user_input)

# ─────────────────────────────────────────────
#  CLEAR BUTTON & FOOTER
# ─────────────────────────────────────────────
if st.session_state.chat:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Clear Conversation", key="clear_btn", use_container_width=True):
            st.session_state.chat = []
            st.rerun()

st.markdown("""
<div class="cs-footer">Protected by Smart AI • Responses are generated automatically</div>
""", unsafe_allow_html=True)