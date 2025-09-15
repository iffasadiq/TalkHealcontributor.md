import streamlit as st

def show_footer():
    st.markdown('''
        <style>
        .footer {
            width: 100%;
            background: rgba(255, 255, 255, 0.15);
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
        <div class="footer">
            <div class="footer-content">
                <div class="footer-col">
                    <h4>Legal</h4>
                    <a href="/PrivacyPolicy" target="_self">Privacy Policy</a><br>
                    <a href="/TermsOfService" target="_self">Terms of Service</a><br>
                    <a href="/Disclaimer" target="_self">Disclaimer</a><br>
                    <a href="/CookiePolicy" target="_self">Cookie Policy</a><br>
                    <a href="/CopyrightNotice" target="_self">Copyright Notice</a>
                </div>
                <div class="footer-col">
                    <h4>Company</h4>
                    <a href="/Blog" target="_self">Blog</a><br>
                    <a href="/Careers" target="_self">Careers</a><br>
                    <a href="/ContactUs" target="_self">Contact Us</a>
                </div>
                <div class="footer-col">
                    <h4>Support</h4>
                    <a href="/HelpCenter" target="_self">Help Center</a><br>
                    <a href="/FAQs" target="_self">FAQs</a>
                </div>
                <div class="footer-col">
                    <h4>Features</h4>
                    <a href="/AppOverview" target="_self">App Overview</a>
                </div>
                <div class="footer-col">
                    <h4>Community & Social</h4>
                    <a href="/Community" target="_self">Community</a><br>
                    <a href="/SocialMedia" target="_self">Social Media</a><br>
                    <a href="/NewsletterSignup" target="_self">Newsletter Signup</a>
                </div>
            </div>
            <div class="footer-tagline">Healing starts here ✨</div>
            <div class="footer-copyright">&copy; 2025 TalkHeal. All rights reserved.</div>
        </div>
    ''', unsafe_allow_html=True)

# Example usage: show_footer() at the end of your main app page
