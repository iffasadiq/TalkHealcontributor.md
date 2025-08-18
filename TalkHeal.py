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

# --- IMPORTS ---
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

# --- 8. FEATURE CARDS LAYOUT FUNCTION ---
def render_feature_cards():
    """Render beautiful feature cards for navigation"""
    
    # Hero Section
    st.markdown(f"""
    <div class="hero-section">
        <h1>🌟 Welcome to TalkHeal, {st.session_state.user_name}!</h1>
        <p>Your comprehensive mental wellness companion with AI-powered support, mindfulness tools, and professional resources.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Actions Row
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🆘 Emergency Help", key="emergency_quick", use_container_width=True, type="secondary"):
            st.session_state.show_emergency_page = True
            st.rerun()
    
    with col2:
        if st.button("💬 Start Chat", key="chat_quick", use_container_width=True):
            st.session_state.show_emergency_page = False
            st.session_state.show_focus_session = False
            st.session_state.show_mood_dashboard = False
            st.rerun()
    
    with col3:
        if st.button("📊 Mood Tracker", key="mood_quick", use_container_width=True):
            st.session_state.show_mood_dashboard = True
            st.rerun()
    
    with col4:
        if st.button("🧘 Focus Session", key="focus_quick", use_container_width=True):
            st.session_state.show_focus_session = True
            st.rerun()
    
    st.markdown("---")
    
    # Main Feature Categories
    st.markdown("### 🌈 Explore Our Wellness Tools")
    
    # Mindfulness & Relaxation Section
    st.markdown("#### 🧘‍♀️ Mindfulness & Relaxation")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card mindfulness-card">
            <div class="card-icon">🧘</div>
            <h3>Yoga Sessions</h3>
            <p>Guided yoga practices for stress relief and mental clarity</p>
            <div class="card-features">
                <span>• Beginner friendly</span><br>
                <span>• Video guides</span><br>
                <span>• Different styles</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Yoga", key="yoga_btn", use_container_width=True):
            st.switch_page("pages/Yoga.py")
    
    with col2:
        st.markdown("""
        <div class="feature-card breathing-card">
            <div class="card-icon">🌬️</div>
            <h3>Breathing Exercises</h3>
            <p>Scientifically-backed breathing techniques for anxiety relief</p>
            <div class="card-features">
                <span>• 4-7-8 Technique</span><br>
                <span>• Box Breathing</span><br>
                <span>• Guided sessions</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Breathing", key="breathing_btn", use_container_width=True):
            st.switch_page("pages/Breathing_Exercise.py")
    
    with col3:
        st.markdown("""
        <div class="feature-card focus-card">
            <div class="card-icon">🎯</div>
            <h3>Focus Sessions</h3>
            <p>Structured meditation and concentration exercises</p>
            <div class="card-features">
                <span>• Timed sessions</span><br>
                <span>• Background sounds</span><br>
                <span>• Progress tracking</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Focus", key="focus_main_btn", use_container_width=True):
            st.session_state.show_focus_session = True
            st.rerun()
    
    # Self-Care & Tracking Section
    st.markdown("#### 📝 Self-Care & Tracking")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card journaling-card">
            <div class="card-icon">📔</div>
            <h3>Digital Journaling</h3>
            <p>Express your thoughts and track your emotional journey</p>
            <div class="card-features">
                <span>• Private & secure</span><br>
                <span>• Mood analysis</span><br>
                <span>• Daily prompts</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Journal", key="journal_btn", use_container_width=True):
            st.switch_page("pages/Journaling.py")
    
    with col2:
        st.markdown("""
        <div class="feature-card mood-card">
            <div class="card-icon">📊</div>
            <h3>Mood Dashboard</h3>
            <p>Visualize your emotional patterns and progress over time</p>
            <div class="card-features">
                <span>• Weekly reports</span><br>
                <span>• Trend analysis</span><br>
                <span>• Insights & tips</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Dashboard", key="dashboard_btn", use_container_width=True):
            st.session_state.show_mood_dashboard = True
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="feature-card selfhelp-card">
            <div class="card-icon">🛠️</div>
            <h3>Self-Help Tools</h3>
            <p>Practical strategies and coping mechanisms for daily challenges</p>
            <div class="card-features">
                <span>• CBT techniques</span><br>
                <span>• Stress management</span><br>
                <span>• Crisis resources</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Tools", key="selfhelp_btn", use_container_width=True):
            st.switch_page("pages/selfHelpTools.py")
    
    # Professional Support Section
    st.markdown("#### 👨‍⚕️ Professional Support")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card doctor-card">
            <div class="card-icon">🩺</div>
            <h3>Find Specialists</h3>
            <p>Connect with mental health professionals in your area</p>
            <div class="card-features">
                <span>• Verified doctors</span><br>
                <span>• Specialty matching</span><br>
                <span>• Contact information</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Find Doctors", key="doctor_btn", use_container_width=True):
            st.switch_page("pages/doctor_spec.py")
    
    with col2:
        st.markdown("""
        <div class="feature-card emergency-card">
            <div class="card-icon">🆘</div>
            <h3>Crisis Support</h3>
            <p>Immediate help and resources for mental health emergencies</p>
            <div class="card-features">
                <span>• 24/7 hotlines</span><br>
                <span>• Local resources</span><br>
                <span>• Safety planning</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Get Help Now", key="crisis_btn", use_container_width=True, type="secondary"):
            st.session_state.show_emergency_page = True
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="feature-card about-card">
            <div class="card-icon">ℹ️</div>
            <h3>About TalkHeal</h3>
            <p>Learn more about our mission and the science behind our tools</p>
            <div class="card-features">
                <span>• Our story</span><br>
                <span>• Research backing</span><br>
                <span>• Team & vision</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Learn More", key="about_btn", use_container_width=True):
            st.switch_page("pages/About.py")

# --- 9. RENDER PAGE CONTENT ---
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
        # Show feature cards layout instead of chat by default
        if st.session_state.get("show_chat_interface", False):
            render_header()
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <h3>🗣️ Current Chatbot Tone: <strong>{st.session_state['selected_tone']}</strong></h3>
            </div>
            """, unsafe_allow_html=True)
            
            # --- Mood Slider ---
            st.subheader("😊 Track Your Mood")
            mood_options = ['Very Sad', 'Sad', 'Neutral', 'Happy', 'Very Happy']
            mood = st.slider(
                'Select your mood',
                min_value=1, max_value=5, value=3, step=1
            )
            coping_tips = {
                1: "It's okay to feel this way. Try some deep breathing exercises to find calm.",
                2: "Consider writing down your thoughts in the journal to process your feelings.",
                3: "A short walk or some light stretching might help you feel balanced.",
                4: "Great to hear you're feeling happy! Share something positive in your journal.",
                5: "You're shining today! Keep spreading that positivity with a kind act."
            }
            st.write(f"Selected mood: {mood_options[mood-1]}")
            st.write(f"Coping tip: {coping_tips.get(mood, 'Let us explore how you are feeling.')}")
            
            render_chat_interface()
            handle_chat_input(model, system_prompt=get_tone_prompt())
            render_session_controls()
        else:
            render_feature_cards()

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