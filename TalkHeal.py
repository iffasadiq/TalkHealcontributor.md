import streamlit as st
import google.generativeai as genai
from auth.auth_utils import init_db
from components.login_page import show_login_page

def set_background_by_mood(mood_scale):
    image_map = {
        1: "https://raw.githubusercontent.com/Martina-stack/TalkHeal-MartinaN/main/dark.png",       # Very Sad
        2: "https://raw.githubusercontent.com/Martina-stack/TalkHeal-MartinaN/main/blue.png",       # Sad
        3: "https://raw.githubusercontent.com/Martina-stack/TalkHeal-MartinaN/main/mint.png",       # Neutral
        4: "https://raw.githubusercontent.com/Martina-stack/TalkHeal-MartinaN/main/lavender.png",   # Happy
        5: "https://raw.githubusercontent.com/Martina-stack/TalkHeal-MartinaN/main/Background.jpg"  # Very Happy
    }
    color_map = {
        1: "#2c3e50",   # dark blue
        2: "#3498db",   # blue
        3: "#a3f7bf",   # mint green
        4: "#b57edc",   # lavender
        5: "#e22bc4"    # pinkish purple
    }

    bg_image = image_map.get(mood_scale, image_map[3])
    bg_color = color_map.get(mood_scale, "#bdc3c7")

    st.markdown(
        f"""
        <style>
        html, body, [data-testid="stApp"] {{
            background-image: url('{bg_image}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-color: {bg_color} !important;
            transition: background-image 0.5s ease-in-out, background-color 0.5s ease-in-out;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(page_title="TalkHeal", page_icon="💬", layout="wide")

# --- DB Initialization ---
if "db_initialized" not in st.session_state:
    try:
        init_db()
        st.session_state["db_initialized"] = True
    except Exception as e:
        st.error(f"Database initialization failed: {e}")
        st.stop()

# --- Auth State Initialization ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

# --- LOGIN PAGE & BACKGROUND ---
if not st.session_state.authenticated:
    # Login page fixed background image
    st.markdown("""
    <style>
    html, body, [data-testid="stApp"] {
        background-image: url('https://raw.githubusercontent.com/Martina-stack/TalkHeal-MartinaN/main/Background.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        height: 100vh;
    }
    </style>
    """, unsafe_allow_html=True)

    show_login_page()
    st.stop()  # This prevents any code below from executing

# --- EVERYTHING BELOW ONLY RUNS AFTER AUTHENTICATION ---

# Import modules only after authentication
from core.utils import save_conversations, load_conversations
from core.config import configure_gemini, PAGE_CONFIG
from core.utils import get_current_time, create_new_conversation
from css.styles import apply_custom_css
from components.header import render_header
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface, handle_chat_input, render_session_controls
from components.mood_dashboard import render_mood_dashboard
from components.emergency_page import render_emergency_page
from components.focus_session import render_focus_session
from components.profile import apply_global_font_size

# --- TOP RIGHT BUTTONS: THEME TOGGLE & LOGOUT ---
col_spacer, col_theme, col_logout = st.columns([5, 0.5, 0.7])
with col_spacer:
    pass
with col_theme:
    is_dark = st.session_state.get('dark_mode', False)
    if st.button("🌙" if is_dark else "☀️", key="top_theme_toggle", help="Toggle Light/Dark Mode", use_container_width=True):
        st.session_state.dark_mode = not is_dark
        st.session_state.theme_changed = True
        st.experimental_rerun()
with col_logout:
    if st.button("Logout", key="logout_btn", use_container_width=True):
        for key in ["authenticated", "user_email", "user_name", "show_signup"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# --- MAIN UI (only after login) ---
header_col1, header_col2, header_col3 = st.columns([6, 1, 1])
with header_col1:
    st.title(f"Welcome to TalkHeal, {st.session_state.user_name}! 💬")
    st.markdown("Navigate to other pages from the sidebar.")

# --- INITIALIZE SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "conversations" not in st.session_state:
    st.session_state.conversations = load_conversations()
if "active_conversation" not in st.session_state:
    st.session_state.active_conversation = -1
if "show_emergency_page" not in st.session_state:
    st.session_state.show_emergency_page = False
if "show_focus_session" not in st.session_state:
    st.session_state.show_focus_session = False
if "show_mood_dashboard" not in st.session_state:
    st.session_state.show_mood_dashboard = False
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"
if "mental_disorders" not in st.session_state:
    st.session_state.mental_disorders = [
        "Depression & Mood Disorders", "Anxiety & Panic Disorders", "Bipolar Disorder",
        "PTSD & Trauma", "OCD & Related Disorders", "Eating Disorders",
        "Substance Use Disorders", "ADHD & Neurodevelopmental", "Personality Disorders",
        "Sleep Disorders"
    ]
if "selected_tone" not in st.session_state:
    st.session_state.selected_tone = "Compassionate Listener"
if "mood" not in st.session_state:
    st.session_state.mood = 3  # Default mood neutral

# --- PAGE CONFIG ---
apply_global_font_size()

# --- APPLY CUSTOM CSS ---
apply_custom_css()
model = configure_gemini()

# --- TONE OPTIONS ---
TONE_OPTIONS = {
    "Compassionate Listener": "You are a compassionate listener — soft, empathetic, patient — like a therapist who listens without judgment.",
    "Motivating Coach": "You are a motivating coach — energetic, encouraging, and action-focused — helping the user push through rough days.",
    "Wise Friend": "You are a wise friend — thoughtful, poetic, and reflective — giving soulful responses and timeless advice.",
    "Neutral Therapist": "You are a neutral therapist — balanced, logical, and non-intrusive — asking guiding questions using CBT techniques.",
    "Mindfulness Guide": "You are a mindfulness guide — calm, slow, and grounding — focused on breathing, presence, and awareness."
}

with st.sidebar:
    st.header("🧠 Choose Your AI Tone")
    selected_tone = st.selectbox(
        "Select a personality tone:",
        options=list(TONE_OPTIONS.keys()),
        index=0
    )
    st.session_state.selected_tone = selected_tone

def get_tone_prompt():
    return TONE_OPTIONS.get(st.session_state.get("selected_tone", "Compassionate Listener"), TONE_OPTIONS["Compassionate Listener"])

render_sidebar()

# --- PAGE ROUTING ---
main_area = st.container()

if not st.session_state.conversations:
    saved_conversations = load_conversations()
    if saved_conversations:
        st.session_state.conversations = saved_conversations
        if st.session_state.active_conversation == -1:
            st.session_state.active_conversation = 0
    else:
        create_new_conversation()
        st.session_state.active_conversation = 0

# --- MOOD BUTTONS & DYNAMIC BACKGROUND ---
with main_area:
    st.subheader("😊 Track Your Mood")

    mood_options = ['Very Sad', 'Sad', 'Neutral', 'Happy', 'Very Happy']
    if 'mood' not in st.session_state:
        st.session_state.mood = 3  # Default mood neutral
 
    cols = st.columns(len(mood_options))
    for i, mood_label in enumerate(mood_options, start=1):
        if cols[i-1].button(mood_label, key=f"mood_btn_{i}"):
            st.session_state.mood = i
            try:
                st.experimental_rerun()
            except Exception:
                pass
  
    set_background_by_mood(st.session_state.mood)

    coping_tips = {
        1: "It's okay to feel this way. Try some deep breathing exercises to find calm.",
        2: "Consider writing down your thoughts in the journal to process your feelings.",
        3: "A short walk or some light stretching might help you feel balanced.",
        4: "Great to hear you're feeling happy! Share something positive in your journal.",
        5: "You're shining today! Keep spreading that positivity with a kind act."
    }

    st.write(f"Selected mood: {mood_options[st.session_state.mood - 1]}")
    st.write(f"Coping tip: {coping_tips[st.session_state.mood]}")

    # Render main UI pages based on flags
    if st.session_state.get("show_emergency_page"):
        render_emergency_page()
    elif st.session_state.get("show_focus_session"):
        render_focus_session()
    elif st.session_state.get("show_mood_dashboard"):
        render_mood_dashboard()
    else:
        render_header()
        st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <h3>🗣️ Current Chatbot Tone: <strong>{st.session_state['selected_tone']}</strong></h3>
            </div>
        """, unsafe_allow_html=True)

        render_chat_interface()
        handle_chat_input(model, system_prompt=get_tone_prompt())
        render_session_controls()

# --- SCROLL TO BOTTOM SCRIPT ---
st.markdown("""
<script>
    function scrollToBottom() {
        var chatContainer = document.querySelector('.chat-container');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }
    setTimeout(scrollToBottom, 100);
</script>
""", unsafe_allow_html=True)
