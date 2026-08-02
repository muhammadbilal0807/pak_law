# components/admin/admin_conversations.py
import streamlit as st
import pandas as pd

def render_admin_conversations(conn):
    """Render the conversations management panel for admins."""
    st.markdown('<div class="admin-header">Conversations Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="admin-subheader">View and manage all user conversations across the platform.</div>', unsafe_allow_html=True)

    # Get all conversations
    df_chats = pd.read_sql_query("""
        SELECT 
            c.id,
            a.email,
            c.title,
            c.mode,
            c.is_pinned,
            c.is_archived,
            c.created_at,
            c.updated_at,
            COUNT(m.id) as message_count
        FROM chats c
        LEFT JOIN accounts a ON c.account_id = a.id
        LEFT JOIN messages m ON c.id = m.chat_id
        GROUP BY c.id
        ORDER BY c.updated_at DESC
        LIMIT 100
    """, conn)

    st.dataframe(df_chats, use_container_width=True, hide_index=True)

    # Conversation details viewer
    st.markdown("### View Conversation Details")
    if not df_chats.empty:
        selected_chat = st.selectbox("Select Conversation", df_chats["id"].tolist())
        if selected_chat:
            messages = pd.read_sql_query("""
                SELECT role, content, tokens, created_at
                FROM messages
                WHERE chat_id = ?
                ORDER BY created_at ASC
            """, conn, params=(selected_chat,))
            
            st.dataframe(messages, use_container_width=True, hide_index=True)