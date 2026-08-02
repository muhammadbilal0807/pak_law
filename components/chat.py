import time
import streamlit as st
from google.genai import types
from config.settings import MAX_HISTORY_MESSAGES, COOLDOWN_SECONDS, MODE_MAX_TOKENS
from services.gemini_service import get_system_instruction, call_gemini_with_retry
from services.category_service import detect_category
from database.db import spend_credit
from utils.markdown_utils import markdown_to_plain

def render_hero():
    """Renders the beautiful empty-state hero screen with prompt suggestions."""
    st.markdown("""
        <div class="animate-fade-in" style="margin-top: 3rem;">
            <div class="hero-title">Ask Anything About <span>Pakistan Law</span></div>
            <div class="hero-subtitle">Get instant, accurate legal references, statutes, and procedural steps.</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-bottom: 2.5rem;'></div>", unsafe_allow_html=True)

    # Feature Cards / Quick Prompts
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🚔 Criminal Law\n\nWhat are my rights upon arrest in Pakistan under the CrPC?"):
            st.session_state.preset_prompt = "What are my fundamental rights upon arrest under the CrPC?"
        if st.button("💻 Cyber Crime\n\nWhat is the punishment for online harassment under PECA?"):
            st.session_state.preset_prompt = "What is the punishment for online harassment and blackmailing under PECA?"
    with c2:
        if st.button("👨‍👩‍👧 Family Law\n\nExplain the procedure for Khula and child custody."):
            st.session_state.preset_prompt = "Explain the legal procedure for Khula and child custody in Pakistan."
        if st.button("🏠 Property Law\n\nHow do I evict a tenant who refuses to pay rent?"):
            st.session_state.preset_prompt = "Under rent control laws, how do I legally evict a defaulting tenant?"
    with c3:
        if st.button("🏛️ Constitution\n\nWhat are the fundamental rights guaranteed by the Constitution?"):
            st.session_state.preset_prompt = "What are the fundamental rights guaranteed by the Constitution of Pakistan 1973?"
        if st.button("💼 Labour Law\n\nWhat is the legal process for wrongful termination?"):
            st.session_state.preset_prompt = "What are the legal remedies for wrongful termination of an employee?"
            
    st.markdown("<div style='margin-bottom: 4rem;'></div>", unsafe_allow_html=True)

def render_chat(app_mode, conn, client, credits_left):
    """Renders the chat interface and handles Gemini API interactions."""
    messages = st.session_state.messages_by_mode[app_mode]
    user_id = st.session_state.user_id

    # Empty State Hero
    if len(messages) == 0 and app_mode == "Legal Q&A":
        render_hero()

    # Render Chat History
    for i, message in enumerate(messages):
        avatar = "👤" if message["role"] == "user" else "⚖️"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            
            # Action Tray for Assistant Messages
            if message["role"] == "assistant":
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f"""
                        <div class="action-tray">
                            <button title="Copy">📋 Copy</button>
                            <button title="Like">👍</button>
                            <button title="Dislike">👎</button>
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    # Native download button integrated seamlessly
                    st.download_button(
                        label="⬇️ Download Document", 
                        data=markdown_to_plain(message["content"]), 
                        file_name=f"pak_law_{app_mode.lower().replace(' ', '_')}_{i}.txt", 
                        key=f"dl_{app_mode}_{i}",
                        type="secondary"
                    )

    # Chat Input Zone
    user_prompt = st.chat_input("Ask anything related to Pakistan law..." if credits_left > 0 else "Limit reached. Please upgrade to continue.")
    
    if st.session_state.get("preset_prompt"):
        user_prompt = st.session_state.preset_prompt
        st.session_state.preset_prompt = None

    if user_prompt:
        if credits_left <= 0:
            st.error("🔒 Free Limit Reached. Please upgrade your plan in the sidebar.")
            st.stop()

        if time.time() - st.session_state.last_request_ts < COOLDOWN_SECONDS:
            st.toast("⏳ Please wait a moment before sending another message.", icon="✋")
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
            with st.spinner("Analyzing legal statutes and drafting response..."):
                try:
                    text, used_model = call_gemini_with_retry(client, formatted_contents, system_instruction, max_tokens)

                    if app_mode == "Legal Q&A":
                        category = detect_category(user_prompt)
                        st.markdown(f"<span style='background:#F1F5F9; color:#0F766E; border: 1px solid #E2E8F0; padding:4px 12px; border-radius:12px; font-size:0.75rem; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;'>🏷️ {category}</span><br><br>", unsafe_allow_html=True)
                    
                    placeholder.markdown(text)
                    messages.append({"role": "assistant", "content": text})
                    spend_credit(conn, user_id, 1)
                    
                    # Force a rerun to render action buttons properly below the new message
                    st.rerun()

                except RuntimeError:
                    placeholder.error(
                        "⚠️ The server is experiencing high traffic. Please try again in 30 seconds."
                    )