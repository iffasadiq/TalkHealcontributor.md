import streamlit as st

def show():
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12); padding: 2.5rem 2.5rem 2rem 2.5rem; margin: 2rem auto; max-width: 900px;'>
            <h2 style='color: #d14a7a; font-family: Baloo 2, cursive;'>Cookie Policy</h2>
            <p style='color: #222; font-size: 1.1rem;'>
                <b>Cookie Policy:</b><br>
                TalkHeal uses cookies and similar technologies to enhance your experience, analyze usage, and improve our services.<br><br>
                <b>What are cookies?</b><br>
                Cookies are small text files stored on your device by your browser. They help us remember your preferences and understand how you use our app.<br><br>
                <b>How we use cookies:</b><br>
                - To keep you signed in<br>
                - To remember your settings<br>
                - To analyze site traffic and usage<br><br>
                <b>Your choices:</b><br>
                You can manage or disable cookies in your browser settings. However, some features may not work properly without cookies.<br><br>
                For more information, contact us at support@talkheal.com.<br><br>
                <i>Last updated: September 2025</i>
            </p>
        </div>
    """, unsafe_allow_html=True)

show()
