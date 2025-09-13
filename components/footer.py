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
            <div style="max-width: 1100px; margin: auto; background: rgba(255, 240, 246, 0.85); border-radius: 18px; box-shadow: 0 2px 18px 0 rgba(255,182,213,0.14); padding: 0.7rem 2.5rem 0.5rem 2.5rem;">
                <div class="footer-content">
                    <div class="footer-col">
                        <h4>Legal</h4>
                        <a href="#">Privacy Policy</a><br>
                        <a href="#">Terms of Service</a><br>
                        <a href="#">Disclaimer</a><br>
                        <a href="#">Cookie Policy</a><br>
                        <a href="#">Copyright Notice</a>
                    </div>
                    <div class="footer-col">
                        <h4>Company</h4>
                        <a href="#">Blog</a><br>
                        <a href="#">Careers</a><br>
                        <a href="#">Contact Us</a>
                    </div>
                    <div class="footer-col">
                        <h4>Support</h4>
                        <a href="#">Help Center</a><br>
                        <a href="#">FAQs</a>
                    </div>
                    <div class="footer-col">
                        <h4>Features</h4>
                        <a href="#">App Overview</a>
                    </div>
                    <div class="footer-col">
                        <h4>Community & Social</h4>
                        <a href="#">Community</a><br>
                        <a href="#">Social Media</a><br>
                        <a href="#">Newsletter Signup</a>
                    </div>
                </div>
                <div class="footer-tagline">Healing starts here ✨</div>
                <div class="footer-copyright">&copy; 2025 TalkHeal. All rights reserved.</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

# Example usage: show_footer() at the end of your main app page
