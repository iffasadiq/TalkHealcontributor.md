import streamlit as st

def show():
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12); padding: 2.5rem 2.5rem 2rem 2.5rem; margin: 2rem auto; max-width: 900px;'>
            <h2 style='color: #d14a7a; font-family: Baloo 2, cursive;'>Community</h2>
            <p style='color: #222; font-size: 1.1rem;'>
                Welcome to the TalkHeal Community!<br><br>
                <b>Connect. Share. Grow.</b><br>
                <ul>
                    <li>Share your mental wellness journey and inspire others.</li>
                    <li>Find encouragement, support, and understanding from fellow members.</li>
                    <li>Participate in community events, challenges, and discussions.</li>
                    <li>Access exclusive resources and group activities.</li>
                </ul>
                <br>
                <b>Why join the TalkHeal Community?</b><br>
                <ul>
                    <li>Safe, inclusive, and non-judgmental space for everyone.</li>
                    <li>Moderated by caring professionals and passionate volunteers.</li>
                    <li>Opportunities to make friends and build lasting connections.</li>
                </ul>
                <br>
                <i>Together, we heal and grow stronger. Join the conversation and be part of something beautiful!</i>
            </p>
        </div>
    """, unsafe_allow_html=True)

show()
import streamlit as st

def show():
    st.title("Community")
    st.write("Join the TalkHeal Community. Details coming soon.")
