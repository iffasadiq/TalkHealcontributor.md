import streamlit as st

def show():
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12); padding: 2.5rem 2.5rem 2rem 2.5rem; margin: 2rem auto; max-width: 900px;'>
            <h2 style='color: #d14a7a; font-family: Baloo 2, cursive;'>Terms of Service</h2>
            <p style='color: #222; font-size: 1.1rem;'>
                Welcome to TalkHeal! By using our app, you agree to the following terms and conditions.<br><br>
                <b>Use of Service:</b><br>
                - You must be at least 13 years old to use TalkHeal.<br>
                - Do not misuse or attempt to disrupt our services.<br><br>
                <b>Content:</b><br>
                - You are responsible for the content you share.<br>
                - Do not share harmful, illegal, or offensive material.<br><br>
                <b>Privacy:</b><br>
                - Your data is handled as described in our Privacy Policy.<br><br>
                <b>Disclaimer:</b><br>
                - TalkHeal is not a substitute for professional medical advice.<br>
                - We do not guarantee uninterrupted service.<br><br>
                <b>Changes:</b><br>
                - Terms may be updated. Continued use means acceptance of changes.<br><br>
                For questions, contact us at support@talkheal.com.<br><br>
                <i>Last updated: September 2025</i>
            </p>
        </div>
    """, unsafe_allow_html=True)

show()
