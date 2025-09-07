# This file handles rendering and managing the "Pinned Messages" page.
import streamlit as st
from datetime import datetime
import base64
from components.chat_interface import toggle_pin_message, inject_custom_css


def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        /* Entire app background */
        html, body, [data-testid="stApp"] {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Sidebar: brighter translucent background */
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.6);
            color: black;
        }}

        /* Header bar: fully transparent */
        [data-testid="stHeader"] {{
            background-color: rgba(0, 0, 0, 0);
        }}

        /* Hide left/right arrow at sidebar bottom */
        button[title="Close sidebar"],
        button[title="Open sidebar"] {{
            display: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set your background image
set_background("static_files/lavender.png")


def render_pinned_messages_page():
    """Render the pinned messages page"""
    st.title("📌 Pinned Messages")
    inject_custom_css()  # load same chat bubble styles

    # Initialize pinned messages if not exists
    if "pinned_messages" not in st.session_state:
        st.session_state.pinned_messages = []

    if not st.session_state.pinned_messages:
        st.markdown("""
        <div style="text-align: center; padding: 40px; background-color: rgba(255,255,255,0.1); border-radius: 15px; margin: 20px 0;">
            <h3>🔖 No Pinned Messages Yet</h3>
            <p>Pin important messages from your conversations to save them here for quick access.</p>
            <p><strong>How to pin:</strong> Look for the 📌 button next to any message in your chat conversations.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Stats section
    total_pinned = len(st.session_state.pinned_messages)
    user_pins = len([msg for msg in st.session_state.pinned_messages if msg.get("sender") == "user"])
    bot_pins = len([msg for msg in st.session_state.pinned_messages if msg.get("sender") == "bot"])

    st.markdown(f"""
    <div style="background-color: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <strong>📊 Your Pinned Messages:</strong> {total_pinned} total | {user_pins} from you | {bot_pins} from TalkHeal
    </div>
    """, unsafe_allow_html=True)

    # Filter options
    col1, col2, col3 = st.columns([2, 2, 6])
    with col1:
        filter_sender = st.selectbox(
            "Filter by:",
            ["All Messages", "My Messages", "TalkHeal Messages"],
            key="pin_filter_sender"
        )

    with col2:
        sort_order = st.selectbox(
            "Sort by:",
            ["Recently Pinned", "Oldest First"],
            key="pin_sort_order"
        )

    # Apply filters
    filtered_messages = st.session_state.pinned_messages.copy()

    if filter_sender == "My Messages":
        filtered_messages = [msg for msg in filtered_messages if msg.get("sender") == "user"]
    elif filter_sender == "TalkHeal Messages":
        filtered_messages = [msg for msg in filtered_messages if msg.get("sender") == "bot"]

    # Apply sorting
    if sort_order == "Recently Pinned":
        filtered_messages.sort(key=lambda x: x.get("pinned_date", ""), reverse=True)
    else:
        filtered_messages.sort(key=lambda x: x.get("pinned_date", ""))

    if not filtered_messages:
        st.info("No messages match your current filter.")
        return

    # Clear all button
    if st.button("🗑️ Clear All Pinned Messages", type="secondary"):
        if st.session_state.get("confirm_clear_pins", False):
            st.session_state.pinned_messages = []
            st.session_state.confirm_clear_pins = False
            st.success("All pinned messages cleared!")
            st.rerun()
        else:
            st.session_state.confirm_clear_pins = True
            st.warning("Click again to confirm clearing all pinned messages.")
            st.rerun()

    st.markdown("---")

    # Render pinned messages using same chat bubble style
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for i, msg in enumerate(filtered_messages):
        sender = msg.get("sender", "bot")
        text = msg.get("message", "")

        if sender == "user":
            st.markdown(f"""
            <div class="user-message">
                {text}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-message">
                {text}
            </div>
            """, unsafe_allow_html=True)

        # Unpin button
        if st.button("❌ Unpin", key=f"unpin_{i}"):
            st.session_state.pinned_messages.remove(msg)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# Main execution
if __name__ == "__main__":
    render_pinned_messages_page()
