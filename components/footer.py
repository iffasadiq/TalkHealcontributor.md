import streamlit as st

def show_footer():
    st.markdown(
        '''
        <style>
        .footer {
            width: 100%;
            background: transparent;
            color: #d14a7a;
            padding: 2rem 0 1rem 0;
            margin-top: 3rem;
            border-top: 2px solid #ffb6d5;
            font-family: 'Baloo 2', cursive;
        }
        .footer-content {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            align-items: flex-start;
            gap: 2rem;
        }
        .footer-col {
            min-width: 160px;
            margin-bottom: 1rem;
        }
        .footer-col h4 {
            font-size: 1.08rem;
            margin-bottom: 0.5rem;
            color: #d14a7a;
            letter-spacing: 1px;
            font-family: 'Baloo 2', cursive;
        }
        .footer-col a {
            color: #d14a7a;
            text-decoration: none;
            transition: color 0.2s;
            font-family: 'Baloo 2', cursive;
            cursor: pointer;
        }
        .footer-col a:hover {
            color: #ff69b4;
        }
        .footer-tagline {
            text-align: center;
            font-size: 1.05rem;
            color: #d14a7a;
            margin-top: 1.2rem;
            font-style: italic;
            font-family: 'Baloo 2', cursive;
        }
        .footer-copyright {
            text-align: center;
            font-size: 0.93rem;
            color: #d14a7a;
            margin-top: 1.2rem;
            font-family: 'Baloo 2', cursive;
        }
        @media (max-width: 700px) {
            .footer-content {
                flex-direction: column;
                align-items: center;
            }
            .footer-col {
                min-width: 80vw;
                text-align: center;
            }
        }
        </style>
        ''', unsafe_allow_html=True)

    cols = st.columns([1,1,1,1,1])
    with cols[0]:
        st.markdown("<h4 style='color:#d14a7a;'>Legal</h4>", unsafe_allow_html=True)
        st.markdown("<a href='/PrivacyPolicy' target='_self' style='color:#d14a7a; text-decoration:none;'>Privacy Policy</a>", unsafe_allow_html=True)
        st.markdown("<a href='/TermsOfService' target='_self' style='color:#d14a7a; text-decoration:none;'>Terms of Service</a>", unsafe_allow_html=True)
        st.markdown("<a href='/Disclaimer' target='_self' style='color:#d14a7a; text-decoration:none;'>Disclaimer</a>", unsafe_allow_html=True)
        st.markdown("<a href='/CookiePolicy' target='_self' style='color:#d14a7a; text-decoration:none;'>Cookie Policy</a>", unsafe_allow_html=True)
        st.markdown("<a href='/CopyrightNotice' target='_self' style='color:#d14a7a; text-decoration:none;'>Copyright Notice</a>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown("<h4 style='color:#d14a7a;'>Company</h4>", unsafe_allow_html=True)
        st.markdown("<a href='#' style='color:#d14a7a;'>Blog</a>", unsafe_allow_html=True)
        st.markdown("<a href='#' style='color:#d14a7a;'>Careers</a>", unsafe_allow_html=True)
        st.markdown("<a href='#' style='color:#d14a7a;'>Contact Us</a>", unsafe_allow_html=True)
    with cols[2]:
        st.markdown("<h4 style='color:#d14a7a;'>Support</h4>", unsafe_allow_html=True)
        st.markdown("<a href='#' style='color:#d14a7a;'>Help Center</a>", unsafe_allow_html=True)
        st.markdown("<a href='#' style='color:#d14a7a;'>FAQs</a>", unsafe_allow_html=True)
    with cols[3]:
        st.markdown("<h4 style='color:#d14a7a;'>Features</h4>", unsafe_allow_html=True)
        st.markdown("<a href='#' style='color:#d14a7a;'>App Overview</a>", unsafe_allow_html=True)
    with cols[4]:
        st.markdown("<h4 style='color:#d14a7a;'>Community & Social</h4>", unsafe_allow_html=True)
        st.markdown("<a href='#' style='color:#d14a7a;'>Community</a>", unsafe_allow_html=True)
        st.markdown("<a href='#' style='color:#d14a7a;'>Social Media</a>", unsafe_allow_html=True)
        st.markdown("<a href='#' style='color:#d14a7a;'>Newsletter Signup</a>", unsafe_allow_html=True)
    st.markdown("<div class='footer-tagline'>Healing starts here ✨</div>", unsafe_allow_html=True)
    st.markdown("<div class='footer-copyright'>&copy; 2025 TalkHeal. All rights reserved.</div>", unsafe_allow_html=True)

# Example usage: show_footer() at the end of your main app page
