import streamlit as st


def show():
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12); padding: 2.5rem 2.5rem 2rem 2.5rem; margin: 2rem auto; max-width: 900px;'>
            <h2 style='color: #d14a7a; font-family: Baloo 2, cursive;'>Connect with TalkHeal on Social Media</h2>
            <div style='color: #222; font-size: 1.1rem;'>
                Stay updated, inspired, and engaged!<br><br>
                <b>Follow us for:</b>
                <ul>
                    <li>Daily wellness tips and motivational posts</li>
                    <li>Community stories and success journeys</li>
                    <li>Live events, Q&A sessions, and more</li>
                </ul>
                <br>
                <b>Our Social Media Channels:</b>
                <ul>
                    <li><a href='https://www.instagram.com/talkheal' target='_blank' style='color:#d14a7a;'>Instagram</a></li>
                    <li><a href='https://www.facebook.com/talkheal' target='_blank' style='color:#d14a7a;'>Facebook</a></li>
                    <li><a href='https://twitter.com/talkheal' target='_blank' style='color:#d14a7a;'>Twitter (X)</a></li>
                    <li><a href='https://www.linkedin.com/company/talkheal' target='_blank' style='color:#d14a7a;'>LinkedIn</a></li>
                    <li><a href='https://www.youtube.com/@talkheal' target='_blank' style='color:#d14a7a;'>YouTube</a></li>
                </ul>
                <br>
                <i>Join our online family and be part of the movement for better mental wellness!</i>
            </div>
        </div>
    """, unsafe_allow_html=True)

show()