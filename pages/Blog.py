import streamlit as st

def show():
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12); padding: 2.5rem 2.5rem 2rem 2.5rem; margin: 2rem auto; max-width: 900px;'>
            <h2 style='color: #d14a7a; font-family: Baloo 2, cursive;'>TalkHeal Blog</h2>
            <div style='color: #000; font-size: 1.1rem;'>
                Welcome to the TalkHeal Blog!<br><br>
                Here you'll find articles, tips, and stories about mental wellness, coping strategies, and community updates.<br><br>
                <b>Latest Posts:</b><br>
                <ul>
                    <li><a href='https://example.com/healing-journey' target='_blank'>How to Start Your Healing Journey</a></li>
                    <li><a href='https://example.com/mindfulness' target='_blank'>Mindfulness for Everyday Life</a></li>
                    <li><a href='https://example.com/community-voices' target='_blank'>Community Voices: Real Stories</a></li>
                </ul>
                <br>
                Stay tuned for more updates and resources.<br><br>
                <i>Content coming soon!</i>
            </div>
        </div>
    """, unsafe_allow_html=True)

show()

