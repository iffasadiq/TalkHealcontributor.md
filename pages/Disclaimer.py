import streamlit as st

def show():
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12); padding: 2.5rem 2.5rem 2rem 2.5rem; margin: 2rem auto; max-width: 900px;'>
            <h2 style='color: #d14a7a; font-family: Baloo 2, cursive;'>Disclaimer</h2>
            <p style='color: #222; font-size: 1.1rem;'>
                <b>Disclaimer:</b><br>
                TalkHeal is designed to provide support and resources for mental wellness. It is not a substitute for professional medical advice, diagnosis, or treatment.<br><br>
                - Always seek the advice of your physician or qualified health provider with any questions you may have regarding a medical condition.<br>
                - Never disregard professional medical advice or delay in seeking it because of something you have read on TalkHeal.<br><br>
                <b>Emergency:</b><br>
                If you are experiencing a medical emergency, call your doctor or emergency services immediately.<br><br>
                <b>Limitation of Liability:</b><br>
                TalkHeal and its creators are not responsible for any decisions made based on the information provided by the app.<br><br>
                For further information, contact us at support@talkheal.com.<br><br>
                <i>Last updated: September 2025</i>
            </p>
        </div>
    """, unsafe_allow_html=True)

show()
