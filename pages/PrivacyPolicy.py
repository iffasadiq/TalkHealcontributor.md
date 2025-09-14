import streamlit as st

def show():
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12); padding: 2.5rem 2.5rem 2rem 2.5rem; margin: 2rem auto; max-width: 900px;'>
            <h2 style='color: #d14a7a; font-family: Baloo 2, cursive;'>Privacy Policy</h2>
            <p style='color: #222; font-size: 1.1rem;'>
                Your privacy is important to us. This Privacy Policy explains how TalkHeal collects, uses, and protects your information.<br><br>
                <b>Information We Collect:</b><br>
                - Personal information you provide (name, email, etc.)<br>
                - Usage data and analytics<br>
                - Cookies and similar technologies<br><br>
                <b>How We Use Information:</b><br>
                - To provide and improve our services<br>
                - To personalize your experience<br>
                - For security and legal compliance<br><br>
                <b>Your Rights:</b><br>
                - Access, update, or delete your data<br>
                - Opt-out of communications<br>
                - Contact us for privacy concerns<br><br>
                For more details, please contact us at support@talkheal.com.<br><br>
                <i>This policy may be updated periodically. Please check back for changes.</i>
            </p>
        </div>
    """, unsafe_allow_html=True)

show()
