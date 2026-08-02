import time
import streamlit as st
from google.genai import types

from config.settings import MAX_HISTORY_MESSAGES, COOLDOWN_SECONDS, MODE_MAX_TOKENS
from services.gemini_service import get_system_instruction, call_gemini_with_retry
from services.category_service import detect_category
from database.db import spend_credit
from utils.markdown_utils import markdown_to_plain

def render_chat(app_mode, conn, client, credits_left):
    """Renders the chat interface and handles Gemini API interactions."""
    messages = st.session_state.messages_by_mode[app_mode]
    user_id = st.session_state.user_id

    # Preset Prompt Suggestions
    if len(messages) == 0 and app_mode == "Legal Q&A":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚨 Rights upon arrest in Pakistan"):
                st.session_state.preset_prompt = "What are my fundamental rights upon arrest?"
        with col2:
            if st.button("💻 Cyber harassment laws (PECA)"):
                st.session_state.preset_prompt = "What is the punishment for cyber harassment under PECA?"

    # Render History
    for message in messages:
        avatar = "👤" if message["role"] == "user" else "⚖️"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Chat Input
    user_prompt = st.chat_input("Ask any legal question..." if credits_left > 0 else "Limit reached. Please upgrade.")
    
    if st.session_state.get("preset_prompt"):
        user_prompt = st.session_state.preset_prompt
        st.session_state.preset_prompt = None

    if user_prompt:
        if credits_left <= 0:
            st.markdown(
                "<div class='paywall-box'><b>🔒 Free Limit Reached.</b><br>"
                "Buy more credits from the sidebar to keep asking questions.</div>",
                unsafe_allow_html=True
            )
            st.stop()

        if time.time() - st.session_state.last_request_ts < COOLDOWN_SECONDS:
            st.info("Please wait a couple of seconds before sending another question.")
            st.stop()

        if len(messages) == 0:
            title = user_prompt[:22] + "..." if len(user_prompt) > 22 else user_prompt
            st.session_state.history_titles.append(f"[{app_mode}] {title}")

        st.chat_message("user", avatar="👤").markdown(user_prompt)
        messages.append({"role": "user", "content": user_prompt})
        st.session_state.last_request_ts = time.time()

        recent_messages = messages[-MAX_HISTORY_MESSAGES:]
        formatted_contents = [
            types.Content(role="user" if m["role"] == "user" else "model", parts=[types.Part.from_text(text=m["content"])])
            for m in recent_messages
        ]

        system_instruction = get_system_instruction(app_mode)
        max_tokens = MODE_MAX_TOKENS[app_mode]

        # Call AI Assistant
        with st.chat_message("assistant", avatar="⚖️"):
            placeholder = st.empty()
            with st.spinner("Analyzing Pakistani legal statutes..."):
                try:
                    text, used_model = call_gemini_with_retry(client, formatted_contents, system_instruction, max_tokens)

                    if app_mode == "Legal Q&A":
                        st.caption(f"🏷️ {detect_category(user_prompt)}")
                    
                    placeholder.markdown(text)
                    st.download_button(
                        "⬇️ Download", 
                        markdown_to_plain(text), 
                        file_name="pak_law_ai_response.txt", 
                        key=f"dl_{app_mode}_{len(messages)}"
                    )

                    messages.append({"role": "assistant", "content": text})
                    spend_credit(conn, user_id, 1)

                except RuntimeError:
                    placeholder.error(
                        "⚠️ Our legal AI is a bit busy right now (high traffic). Please wait 30 seconds "
                        "and try again. If this keeps happening, message us on WhatsApp from the sidebar."
                    )