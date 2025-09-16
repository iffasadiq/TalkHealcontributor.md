import streamlit as st

def show_app_overview():
    st.markdown("""
        <div style='background-color: #ffe4ef; border-radius: 15px; padding: 2rem; margin-bottom: 2rem;'>
            <h2 style='color: #d6336c; text-align: center;'>App Overview</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style='background-color: #fff; border-radius: 10px; box-shadow: 0 2px 8px #d6336c22; padding: 2rem; margin-bottom: 2rem;'>
            <h3 style='color: #d6336c;'>Welcome to TalkHeal!</h3>
            <p style='color: #222;'>
                TalkHeal is your trusted companion for mental wellness, designed to empower you on your journey to emotional health.<br><br>
                <b>Key Features:</b>
                <ul>
                    <li><b>Mood Tracking:</b> Visualize your emotional patterns.</li>
                    <li><b>Coping Tools:</b> Breathing exercises & journaling.</li>
                    <li><b>Resource Hub:</b> Articles, guides, expert advice.</li>
                    <li><b>Community Support:</b> Safe, inclusive space.</li>
                    <li><b>Dashboard:</b> Track progress and achievements.</li>
                </ul>
                <br>
                <b>Why TalkHeal?</b><br>
                <ul>
                    <li>Soothing, user-friendly design.</li>
                    <li>Privacy-first, secure data.</li>
                    <li>Works on all devices.</li>
                    <li>Free to start, premium for more.</li>
                </ul>
                <br>
                <b>Start your journey with TalkHeal and discover a happier, healthier you!</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

# 🔹 Call function so Streamlit actually runs it
show_app_overview()
