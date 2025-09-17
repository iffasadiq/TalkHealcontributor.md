import streamlit as st

def show():
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffe4f0 0%, #fff 100%); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(209,74,122,0.12); padding: 2.5rem 2.5rem 2rem 2.5rem; margin: 2rem auto; max-width: 900px;'>
            <h2 style='color: #d14a7a; font-family: Baloo 2, cursive;'>Subscribe to the TalkHeal Newsletter</h2>
            <p style='color: #222; font-size: 1.1rem;'>
                Get the latest updates, wellness tips, and exclusive content delivered straight to your inbox!<br><br>
                <b>Sign up below to join our community:</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

    with st.form(key="newsletter_form"):
        email = st.text_input("Email Address", placeholder="Enter your email", key="newsletter_email")
        submit = st.form_submit_button("Subscribe", help="Sign up for our newsletter")
        if submit:
            if email and "@" in email and "." in email:
                st.success("Thank you for subscribing! You'll receive our next newsletter soon.")
            else:
                st.error("Please enter a valid email address.")

show()

def show():
    st.title("Newsletter Signup")
    st.write("Sign up for the TalkHeal newsletter. Form coming soon.")
