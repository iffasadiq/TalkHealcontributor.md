import streamlit as st

def show():
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12); padding: 2.5rem 2.5rem 2rem 2.5rem; margin: 2rem auto; max-width: 900px;'>
            <h2 style='color: #d14a7a; font-family: Baloo 2, cursive;'>Copyright Notice</h2>
            <p style='color: #222; font-size: 1.1rem;'>
                <b>Copyright Notice:</b><br>
                &copy; 2025 TalkHeal. All rights reserved.<br><br>
                All content, design, graphics, and code on this app are the property of TalkHeal and its creators unless otherwise stated.<br><br>
                Unauthorized use, reproduction, or distribution of any material from this app is strictly prohibited.<br><br>
                For permissions or inquiries, contact us at support@talkheal.com.<br><br>
                <i>Last updated: September 2025</i>
            </p>
        </div>
    """, unsafe_allow_html=True)

show()
