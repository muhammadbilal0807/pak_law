import streamlit as st
from streamlit_option_menu import option_menu
from database.db import get_chats_for_user, create_chat

def render_sidebar(conn, credits_left):
    with st.sidebar:
        st.markdown("<div class='sidebar-logo animate-fade-in'>⚖️ Pak Law AI</div>", unsafe_allow_html=True)
        
        # New Chat System
        if st.button("➕ New Conversation", type="primary", use_container_width=True):
            st.session_state.current_chat_id = None
            st.session_state.messages_by_mode = [] # Clear current view
            st.rerun()

        st.markdown(f"""
            <div class="credit-card" style="margin-top: 1rem;">
                <div class="credit-title">Available Credits</div>
                <div class="credit-value">{max(credits_left, 0)}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 1rem 0; border-color: #E5E7EB;'>", unsafe_allow_html=True)
        
        # Main Navigation
        app_mode = option_menu(
            menu_title="WORKSPACE",
            options=["Legal Q&A", "Drafting", "Analysis", "Bookmarks", "Profile", "Settings"],
            icons=['chat-left-text', 'file-earmark-text', 'search', 'bookmark', 'person', 'gear'],
            default_index=0,
            styles={
                "menu-title": {"font-size": "12px", "color": "#6B7280", "font-weight": "600"},
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#6B7280", "font-size": "16px"}, 
                "nav-link": {"font-size": "14px", "margin":"5px 0", "color": "#111827"},
                "nav-link-selected": {"background-color": "#E0F2FE", "color": "#0F766E", "font-weight": "600"},
            }
        )

        st.markdown("<hr style='margin: 1rem 0; border-color: #E5E7EB;'>", unsafe_allow_html=True)
        
        # Persistent Chat History
        st.markdown("<span style='color:#6B7280; font-size:12px; font-weight:600;'>RECENT CHATS</span>", unsafe_allow_html=True)
        recent_chats = get_chats_for_user(conn, st.session_state.user["id"])
        
        for chat_id, title, mode, is_pinned in recent_chats[:10]:
            icon = "📌" if is_pinned else "💬"
            if st.button(f"{icon} {title[:25]}...", key=f"hist_{chat_id}", use_container_width=True):
                st.session_state.current_chat_id = chat_id
                st.session_state.current_mode = mode
                st.rerun()

    return app_mode