import streamlit as st

def show():
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12); padding: 2.5rem 2.5rem 2rem 2.5rem; margin: 2rem auto; max-width: 900px;'>
            <h2 style='color: #d14a7a; font-family: Baloo 2, cursive;'>Careers at TalkHeal</h2>
            <div style='color: #000; font-size: 1.1rem;'>
                Join our mission to support mental wellness!<br><br>
                <b>Current Openings:</b><br>
                <ul>
                    <li>Community Manager</li>
                    <li>Content Writer (Mental Health)</li>
                    <li>Full Stack Developer</li>
                    <li>UI/UX Designer</li>
                </ul>
                <br>
                If you are passionate about mental health and want to make a difference, send your resume to <a href='mailto:careers@talkheal.com'>careers@talkheal.com</a>.<br><br>
                <i>More roles and details coming soon!</i>
            </div>
        </div>
    """, unsafe_allow_html=True)

show()
