import streamlit as st
import google.generativeai as genai
from auth.auth_utils import init_db
from components.login_page import show_login_page

st.set_page_config(page_title="TalkHeal", page_icon="💬", layout="wide")

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
    col_spacer, col_theme, col_logout = st.columns([5, 0.5, 0.7])
    with col_spacer:
        pass  # empty spacer to push buttons right
    with col_theme:
        is_dark = st.session_state.get('dark_mode', False)
        if st.button("🌙" if is_dark else "☀️", key="top_theme_toggle", help="Toggle Light/Dark Mode", use_container_width=True):
            st.session_state.dark_mode = not is_dark
            st.session_state.theme_changed = True
            st.rerun()
    with col_logout:
        if st.button("Logout", key="logout_btn", use_container_width=True):
            for key in ["authenticated", "user_email", "user_name", "show_signup"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

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
            <h1 class="hero-title">Welcome to TalkHeal, {st.session_state.user_name}! 💬</h1>
            <p class="hero-subtitle">Your comprehensive mental wellness companion with AI-powered support and therapeutic tools</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Current AI Tone Display
    st.markdown(f"""
    <div class="current-tone-display">
        <div class="tone-content">
            <span class="tone-label">🧠 Current AI Personality:</span>
            <span class="tone-value">{st.session_state['selected_tone']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Feature Cards Grid
    st.markdown('<div class="features-grid-container">', unsafe_allow_html=True)
    
    # Row 1: Primary Features
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card primary-card yoga-card">
            <div class="card-icon">🧘‍♀️</div>
            <h3>Yoga & Meditation</h3>
            <p>Guided yoga sessions and mindfulness practices for inner peace</p>
            <div class="card-features">
                <span>• Guided Sessions</span>
                <span>• Mindfulness Training</span>
                <span>• Stress Relief</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🧘‍♀️ Start Yoga", key="yoga_btn", use_container_width=True):
            st.switch_page("pages/Yoga.py")
    
    with col2:
        st.markdown("""
        <div class="feature-card primary-card breathing-card">
            <div class="card-icon">🌬️</div>
            <h3>Breathing Exercises</h3>
            <p>Therapeutic breathing techniques to calm your mind instantly</p>
            <div class="card-features">
                <span>• 4-7-8 Breathing</span>
                <span>• Box Breathing</span>
                <span>• Anxiety Relief</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🌬️ Start Breathing", key="breathing_btn", use_container_width=True):
            st.switch_page("pages/Breathing_Exercise.py")
    
    with col3:
        st.markdown("""
        <div class="feature-card primary-card journal-card">
            <div class="card-icon">📝</div>
            <h3>Personal Journaling</h3>
            <p>Express your thoughts and track your emotional journey</p>
            <div class="card-features">
                <span>• Daily Reflections</span>
                <span>• Mood Tracking</span>
                <span>• Progress Insights</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 Open Journal", key="journal_btn", use_container_width=True):
            st.switch_page("pages/Journaling.py")
    
    # Row 2: Secondary Features
    col4, col5 = st.columns([1, 1])
    
    with col4:
        st.markdown("""
        <div class="feature-card secondary-card doctor-card">
            <div class="card-icon">👨‍⚕️</div>
            <h3>Doctor Specialist Finder</h3>
            <p>Connect with mental health professionals in your area</p>
            <div class="card-features">
                <span>• Specialist Directory</span>
                <span>• Location-based Search</span>
                <span>• Professional Profiles</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("👨‍⚕️ Find Specialists", key="doctor_btn", use_container_width=True):
            st.switch_page("pages/doctor_spec.py")
    
    with col5:
        st.markdown("""
        <div class="feature-card secondary-card tools-card">
            <div class="card-icon">🛠️</div>
            <h3>Self-Help Tools</h3>
            <p>Comprehensive toolkit for mental wellness and self-care</p>
            <div class="card-features">
                <span>• Coping Strategies</span>
                <span>• Wellness Activities</span>
                <span>• Resource Library</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🛠️ Explore Tools", key="tools_btn", use_container_width=True):
            st.switch_page("pages/selfHelpTools.py")
    
    # Row 3: Dashboard Features (Wider Cards)
    col6, col7 = st.columns([1, 1])
    
    with col6:
        st.markdown("""
        <div class="feature-card dashboard-card mood-card">
            <div class="card-icon-large">📊</div>
            <h3>Mood Dashboard</h3>
            <p>Visualize your emotional patterns and mental health progress</p>
            <div class="card-stats">
                <div class="stat">
                    <span class="stat-number">7</span>
                    <span class="stat-label">Day Tracking</span>
                </div>
                <div class="stat">
                    <span class="stat-number">∞</span>
                    <span class="stat-label">Insights</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 View Dashboard", key="mood_dashboard_btn", use_container_width=True):
            st.session_state.show_mood_dashboard = True
            st.rerun()
    
    with col7:
        st.markdown("""
        <div class="feature-card dashboard-card focus-card">
            <div class="card-icon-large">🎯</div>
            <h3>Focus Sessions</h3>
            <p>Structured mindfulness and concentration exercises</p>
            <div class="card-stats">
                <div class="stat">
                    <span class="stat-number">25</span>
                    <span class="stat-label">Min Sessions</span>
                </div>
                <div class="stat">
                    <span class="stat-number">+</span>
                    <span class="stat-label">Focus Boost</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎯 Start Focus", key="focus_btn", use_container_width=True):
            st.session_state.show_focus_session = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Emergency Support Section
    st.markdown("""
    <div class="emergency-support-section">
        <div class="emergency-content">
            <h3>🚨 Need Immediate Support?</h3>
            <p>Get instant access to crisis resources and emergency mental health support</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚨 Emergency Resources", key="emergency_main_btn", use_container_width=True, type="secondary"):
        st.session_state.show_emergency_page = True
        st.rerun()

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
        
        # Mood Tracking Section
        st.markdown("---")
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
        render_header()
        render_chat_interface()
        handle_chat_input(model, system_prompt=get_tone_prompt())
        render_session_controls()

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