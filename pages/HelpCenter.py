import streamlit as st

def show():
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12); padding: 2.5rem 2.5rem 2rem 2.5rem; margin: 2rem auto; max-width: 900px;'>
            <h2 style='color: #d14a7a; font-family: Baloo 2, cursive;'>Help Center</h2>
            <p style='color: #222; font-size: 1.1rem;'>
                Welcome to the TalkHeal Help Center!<br><br>
                <b>How can we assist you?</b><br>
                <ul>
                    <li><b>Getting Started:</b> Learn how to use TalkHeal and explore its features.</li>
                    <li><b>Account & Privacy:</b> Manage your profile, privacy settings, and data.</li>
                    <li><b>AI Companion:</b> Tips for interacting with your AI and customizing its tone.</li>
                    <li><b>Wellness Tools:</b> Discover yoga, journaling, breathing exercises, and more.</li>
                    <li><b>Support & Feedback:</b> Reach out for help or share your suggestions.</li>
                </ul>
                <br>
                <b>Why TalkHeal?</b><br>
                TalkHeal is your trusted mental health companion, offering a safe, supportive, and beautifully designed space for healing and growth. Our features are crafted with care, and our community is here to uplift you.<br><br>
                <b>Need more help?</b><br>
                Email us at <a href='mailto:support@talkheal.com'>support@talkheal.com</a> or visit the <a href='/FAQs' target='_self'>FAQs</a> page.<br><br>
                <i>We're here for you, every step of the way!</i>
            </p>
        </div>
    """, unsafe_allow_html=True)

show()
