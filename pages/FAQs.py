import streamlit as st

def show():
    st.markdown("""
        <div style='background-color: #ffe4ef; border-radius: 15px; padding: 2rem; margin-bottom: 2rem;'>
            <h2 style='color: #d6336c; text-align: center;'>Frequently Asked Questions (FAQs)</h2>
        </div>
    """, unsafe_allow_html=True)

    faqs = [
        {
            "question": "What is TalkHeal?",
            "answer": "TalkHeal is a supportive mental wellness platform offering mood tracking, coping tools, and expert resources to help you thrive."
        },
        {
            "question": "Is my data private and secure?",
            "answer": "Absolutely! We use advanced security measures to keep your information confidential and safe."
        },
        {
            "question": "How do I use the mood tracking feature?",
            "answer": "Simply log in, navigate to the Mood Dashboard, and record your feelings daily. Visual insights help you understand your emotional patterns."
        },
        {
            "question": "Can I access TalkHeal on mobile devices?",
            "answer": "Yes, TalkHeal is fully responsive and works seamlessly on smartphones, tablets, and desktops."
        },
        {
            "question": "Are there professional resources available?",
            "answer": "Yes! Explore our Wellness Resource Hub for expert articles, self-help tools, and contact information for specialists."
        },
        {
            "question": "How do I contact support?",
            "answer": "Visit our Help Center or use the Contact Us page for quick assistance. Our team is here to help you 24/7."
        },
        {
            "question": "Is TalkHeal free to use?",
            "answer": "Most features are free. Some premium resources may require a subscription, but you can get started at no cost!"
        }
    ]


    for faq in faqs:
        st.markdown(f"""
            <div style='background-color: #fff; border-radius: 10px; box-shadow: 0 2px 8px #d6336c22; padding: 1.5rem; margin-bottom: 1.5rem;'>
                <h4 style='color: #d6336c;'>{faq['question']}</h4>
                <p style='color: #222;'>{faq['answer']}</p>
            </div>
        """, unsafe_allow_html=True)

show()
