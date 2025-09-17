import streamlit as st

def show():
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12); padding: 2.5rem 2.5rem 2rem 2.5rem; margin: 2rem auto; max-width: 900px;'>
            <h2 style='color: #d14a7a; font-family: Baloo 2, cursive;'>Contact Us</h2>
            <p style='color: #222; font-size: 1.1rem;'>
                We'd love to hear from you!<br><br>
                <b>Email:</b> <a href='mailto:support@talkheal.com'>support@talkheal.com</a><br>
                <b>Careers:</b> <a href='mailto:careers@talkheal.com'>careers@talkheal.com</a><br>
                <b>Community:</b> <a href='mailto:community@talkheal.com'>community@talkheal.com</a><br><br>
                <b>Social Media:</b><br>
                <a href='https://instagram.com/talkheal' target='_blank'>Instagram</a> | <a href='https://twitter.com/talkheal' target='_blank'>Twitter</a> | <a href='https://facebook.com/talkheal' target='_blank'>Facebook</a><br><br>
                <i>We aim to respond within 2 business days.</i>
            </p>
        </div>
    """, unsafe_allow_html=True)

show()
