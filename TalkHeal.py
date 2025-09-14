import streamlit as st
from auth.auth_utils import init_db
from components.login_page import show_login_page
from core.utils import save_conversations, load_conversations


# HANDLES ALL SESSION STATE VALUES
def init_session_state(): 
    defaults = { "chat_history": [],
                "conversations": load_conversations(), 
                "active_conversation": 0, 
                "selected_tone": "Compassionate Listener",
                "show_emergency_page": False,
                "show_focus_session": False,
                "show_mood_dashboard": False } 
    for key, value in defaults.items(): 
        if key not in st.session_state: 
            st.session_state[key] = value 
init_session_state()

st.set_page_config(page_title="TalkHeal", page_icon="💬", layout="wide")

no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# --- DB Initialization ---
if "db_initialized" not in st.session_state:
    init_db()
    st.session_state["db_initialized"] = True

# --- Auth State Initialization ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

# --- LOGIN PAGE ---
if not st.session_state.authenticated:
    show_login_page()
    st.stop()

# --- TOP RIGHT BUTTONS: THEME TOGGLE & LOGOUT ---
if st.session_state.get("authenticated", False):
    col_spacer, col_theme, col_emergency, col_about, col_logout = st.columns([0.7, 0.1, 0.35, 0.2, 0.2])
    with col_spacer:
        pass
    with col_theme:
        is_dark = st.session_state.get('dark_mode', False)
        if st.button("🌙" if is_dark else "☀️", key="top_theme_toggle", help="Toggle Light/Dark Mode", use_container_width=True):
            st.session_state.dark_mode = not is_dark
            st.session_state.theme_changed = True
            st.rerun()
    with col_emergency:
        if st.button("🚨 Emergency Help", key="emergency_main_btn", help="Open crisis resources", use_container_width=True, type="secondary"):
            st.session_state.show_emergency_page = True
            st.rerun()
    with col_about:
        if st.button("ℹ️ About", key="about_btn", help="About TalkHeal", use_container_width=True):
            st.switch_page("pages/About.py")
    with col_logout:
        if st.button("Logout", key="logout_btn", help="Sign out", use_container_width=True):
            for key in ["authenticated", "user_email", "user_name", "show_signup"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

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

# --- 1. INITIALIZE SESSION STATE ---
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
if "pinned_messages" not in st.session_state:
    st.session_state.pinned_messages = []

if "active_page" not in st.session_state:
    st.session_state.active_page = "TalkHeal"  # default

# --- Footer Navigation State ---
if "show_privacy_policy" not in st.session_state:
    st.session_state.show_privacy_policy = False

if st.session_state.show_privacy_policy:
    from pages.PrivacyPolicy import show as show_privacy
    show_privacy()
    from components.footer import show_footer
    show_footer()
    st.stop()

# --- 2. SET PAGE CONFIG ---
apply_global_font_size()

# --- 3. APPLY STYLES & CONFIGURATIONS ---
apply_custom_css()
model = configure_gemini()

# --- 4. TONE SELECTION DROPDOWN IN SIDEBAR ---
TONE_OPTIONS = {
    "Compassionate Listener": "You are a compassionate listener — soft, empathetic, patient — like a therapist who listens without judgment.",
    "Motivating Coach": "You are a motivating coach — energetic, encouraging, and action-focused — helping the user push through rough days.",
    "Wise Friend": "You are a wise friend — thoughtful, poetic, and reflective — giving soulful responses and timeless advice.",
    "Neutral Therapist": "You are a neutral therapist — balanced, logical, and non-intrusive — asking guiding questions using CBT techniques.",
    "Mindfulness Guide": "You are a mindfulness guide — calm, slow, and grounding — focused on breathing, presence, and awareness."
}

# --- 5. DEFINE FUNCTION TO GET TONE PROMPT ---
def get_tone_prompt():
    return TONE_OPTIONS.get(st.session_state.get("selected_tone", "Compassionate Listener"), TONE_OPTIONS["Compassionate Listener"])

# --- 6. RENDER SIDEBAR ---
render_sidebar()

# --- 7. PAGE ROUTING ---
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
    st.rerun()

# --- 8. FEATURE CARDS FUNCTION ---
def render_feature_cards():
    """Render beautiful feature cards showcasing app capabilities"""
    
    # Hero Welcome Section
    st.markdown(f"""
    <div class="hero-welcome-section">
        <div class="hero-content">
            <h1 class="hero-title">Welcome to TalkHeal, 
            {st.session_state.user_profile.get("name", "User")}! 💬</h1>
            <p class="hero-subtitle">Your Mental Health Companion 💙</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Feature Cards Grid
    st.markdown('<div class="features-grid-container">', unsafe_allow_html=True)
    
    # Row 1: Primary Features
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card primary-card yoga-card">
            <div class="card-icon">🧘‍♀️</div>
            <h3>Yoga & Meditation</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🧘‍♀️ Start Yoga", key="yoga_btn", use_container_width=True):
            st.switch_page("pages/Yoga.py")
    
    with col2:
        st.markdown("""
        <div class="feature-card primary-card breathing-card">
            <div class="card-icon">🌬️</div>
            <h3>Breathing Exercises</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌬️ Start Breathing", key="breathing_btn", use_container_width=True):
            st.switch_page("pages/Breathing_Exercise.py")
    
    with col3:
        st.markdown("""
        <div class="feature-card primary-card journal-card">
            <div class="card-icon">📝</div>
            <h3>Personal Journaling</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📝 Open Journal", key="journal_btn", use_container_width=True):
            st.switch_page("pages/Journaling.py")
    
    with col4:
        st.markdown("""
        <div class="feature-card primary-card doctor-card">
            <div class="card-icon">👨‍⚕️</div>
            <h3>Doctor Specialist</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👨‍⚕️ Find Specialists", key="doctor_btn", use_container_width=True):
            st.switch_page("pages/doctor_spec.py")
    
    with col5:
        st.markdown("""
        <div class="feature-card secondary-card tools-card">
            <div class="card-icon">🛠️</div>
            <h3>Self-Help Tools</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🛠️ Explore Tools", key="tools_btn", use_container_width=True):
            st.switch_page("pages/selfHelpTools.py")
    
    with col6:
        st.markdown("""
        <div class="feature-card secondary-card wellness-card">
            <div class="card-icon">🌿</div>
            <h3>Wellness Hub</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌿 Open Wellness Hub", key="wellness_btn", use_container_width=True):
            st.switch_page("pages/WellnessResourceHub.py")
    
    st.markdown('</div>', unsafe_allow_html=True)


# --- 9. RENDER PAGE ---
if st.session_state.get("show_emergency_page"):
    with main_area:
        render_emergency_page()
elif st.session_state.get("show_focus_session"):
    with main_area:
        render_focus_session()
elif st.session_state.get("show_mood_dashboard"):
    with main_area:
        render_mood_dashboard()

# Handles rendering the "Pinned Messages" page.
elif st.session_state.active_page == "PinnedMessages":
    with main_area:
        from pages.Pinned_msg import render_pinned_messages_page

        # Back to Home Button
        if st.button("⬅ Back to Home", key="back_to_home_btn"):
            st.session_state.active_page = "TalkHeal"
            st.rerun()

        render_pinned_messages_page()

else:
    with main_area:
        # Render the beautiful feature cards layout
        render_feature_cards()
        
        # AI Tone Selection in main area
        with st.expander("🧠 Customize Your AI Companion", expanded=False):
            st.markdown("**Choose how your AI companion should respond to you:**")
            selected_tone = st.selectbox(
                "Select AI personality:",
                options=list(TONE_OPTIONS.keys()),
                index=list(TONE_OPTIONS.keys()).index(st.session_state.selected_tone),
                help="Different tones provide different therapeutic approaches"
            )
            if selected_tone != st.session_state.selected_tone:
                st.session_state.selected_tone = selected_tone
                st.rerun()
            
            st.info(f"**Current Style**: {TONE_OPTIONS[selected_tone]}")
            
        # Current AI Tone Display
        st.markdown(f"""
        <div class="current-tone-display">
            <div class="tone-content">
                <span class="tone-label">🧠 Current AI Personality:</span>
                <span class="tone-value">{st.session_state['selected_tone']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
        # Mood Tracking Section
        st.markdown("""
        <div class="mood-tracking-section">
            <h3>😊 How are you feeling today?</h3>
            <p>Track your mood to help your AI companion provide better support</p>
        </div>
        """, unsafe_allow_html=True)
        
        mood_options = ['Very Sad 😢', 'Sad 😔', 'Neutral 😐', 'Happy 😊', 'Very Happy 😄']
        mood = st.slider(
            'Select your current mood',
            min_value=1, max_value=5, value=3, step=1,
            format="",
            help="This helps personalize your AI conversation"
        )
        
        coping_tips = {
            1: "🤗 It's okay to feel this way. Try some deep breathing exercises to find calm.",
            2: "📝 Consider writing down your thoughts in the journal to process your feelings.",
            3: "🚶‍♀️ A short walk or some light stretching might help you feel balanced.",
            4: "✨ Great to hear you're feeling happy! Share something positive in your journal.",
            5: "🌟 You're shining today! Keep spreading that positivity with a kind act."
        }
        
        col_mood, col_tip = st.columns([1, 2])
        with col_mood:
            st.markdown(f"**Current mood**: {mood_options[mood-1]}")
        with col_tip:
            st.info(coping_tips.get(mood, 'Let\'s explore how you\'re feeling.'))
        
        st.markdown("---")
        
        # Chat Interface
        # render_header()
        render_chat_interface()
        handle_chat_input(model, system_prompt=get_tone_prompt())
        render_session_controls()

        # --- Footer ---
        from components.footer import show_footer
        show_footer()

# --- 10. SCROLL SCRIPT ---
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
