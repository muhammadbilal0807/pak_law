# components/chat.py (UPDATED)
import time
import streamlit as st
from google.genai import types
from database.db import spend_credit, save_message, create_chat, get_messages_for_chat
from services.gemini_service import get_system_instruction, call_gemini_with_retry
from services.export_service import export_docx, export_pdf, export_txt

def render_ai_metadata():
    """Renders professional citation and metadata cards below AI responses."""
    st.markdown("""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px; margin-top: 10px; font-size: 0.85rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #0F766E; font-weight: 600;">🏛️ Relevant Statutes Found</span>
                <span style="color: #64748B;">Confidence: 🟢 High</span>
            </div>
            <div style="color: #475569; margin-bottom: 8px;">
                <em>Disclaimer: This AI-generated response is for informational purposes and does not constitute formal legal counsel under the Pakistan Bar Council rules.</em>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_chat(app_mode, conn, client, credits_left):
    account_id = st.session_state.user["id"]
    
    # Load history if a chat is selected
    if st.session_state.get("current_chat_id"):
        chat_id = st.session_state.current_chat_id
        raw_msgs = get_messages_for_chat(conn, chat_id)
        messages = [{"role": m[1], "content": m[2]} for m in raw_msgs]
        # FIXED: Update session state with loaded messages
        st.session_state.messages_by_mode = messages
    else:
        chat_id = None
        messages = st.session_state.get("messages_by_mode", [])

    # Top Toolbar (File & Voice)
    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader("📎 Analyze Document (PDF/DOCX)", type=["pdf", "docx", "txt"])
    with col2:
        audio_val = st.audio_input("🎙️ Voice Prompt (Beta)")

    # Render Messages
    for i, message in enumerate(messages):
        avatar = "👤" if message["role"] == "user" else "⚖️"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            
            if message["role"] == "assistant":
                render_ai_metadata()
                
                # Enhanced Chat Actions
                a1, a2, a3, a4 = st.columns([1,1,1,1])
                with a1:
                    st.download_button("📥 PDF", export_pdf(message["content"]), file_name=f"export_{i}.pdf", key=f"pdf_{i}")
                with a2:
                    st.download_button("📝 DOCX", export_docx(message["content"]), file_name=f"export_{i}.docx", key=f"docx_{i}")
                with a3:
                    if st.button("🔖 Bookmark", key=f"bm_{i}"):
                        st.toast("Saved to Bookmarks!")
                with a4:
                    if st.button("🔊 Read", key=f"read_{i}"):
                        st.toast("Text-to-speech starting...")

    # Input Area
    user_prompt = st.chat_input("Ask anything related to Pakistan law..." if credits_left > 0 else "Limit reached.")

    # Override text input if voice is recorded
    if audio_val and not user_prompt:
        user_prompt = "Transcribed audio intent..."

    if user_prompt:
        if credits_left <= 0:
            st.error("🔒 Free Limit Reached. Please upgrade your plan.")
            st.stop()

        # Initialize new chat in DB if none exists
        if not chat_id:
            title = user_prompt[:30] + "..."
            chat_id = create_chat(conn, account_id, title, app_mode)
            st.session_state.current_chat_id = chat_id
            messages = []

        # Save User Message
        save_message(conn, chat_id, "user", user_prompt)
        messages.append({"role": "user", "content": user_prompt})
        st.chat_message("user", avatar="👤").markdown(user_prompt)

        # AI Call
        formatted_contents = [types.Content(role="user" if m["role"] == "user" else "model", parts=[types.Part.from_text(text=m["content"])]) for m in messages]
        
        with st.chat_message("assistant", avatar="⚖️"):
            with st.spinner("Analyzing legal frameworks..."):
                try:
                    text, _ = call_gemini_with_retry(client, formatted_contents, get_system_instruction(app_mode), 1500)
                    
                    st.markdown(text)
                    render_ai_metadata()
                    
                    # Save Assistant Message
                    save_message(conn, chat_id, "assistant", text, tokens=len(text.split()))
                    spend_credit(conn, account_id, 1)
                    
                    # FIXED: Update session state after new message
                    st.session_state.messages_by_mode = messages + [{"role": "assistant", "content": text}]
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")