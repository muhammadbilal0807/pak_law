import streamlit as st
from streamlit_option_menu import option_menu

def render_admin_sidebar():
    with st.sidebar:
        st.markdown("""
            <div style="font-size:1.3rem; font-weight:700; color:#38BDF8; margin-bottom:1.5rem; display:flex; align-items:center; gap:8px;">
                ⚡ Admin Console
            </div>
        """, unsafe_allow_html=True)
        
        # Admin Menu Options
        admin_tab = option_menu(
            menu_title="MANAGEMENT",
            options=[
                "Overview", 
                "User Control", 
                "Conversations", 
                "Law Database", 
                "Knowledge Base", 
                "Prompts & AI Config", 
                "Analytics", 
                "Payments & Plans", 
                "System & Security"
            ],
            icons=['speedometer2', 'people', 'chat-dots', 'journal-text', 'file-earmark-code', 'cpu', 'graph-up-arrow', 'credit-card', 'shield-lock'],
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#94A3B8", "font-size": "15px"}, 
                "nav-link": {"font-size": "13px", "margin":"3px 0", "color": "#CBD5E1"},
                "nav-link-selected": {"background-color": "#0284C7", "color": "#FFFFFF", "font-weight": "600"},
            }
        )

        st.markdown("<hr style='border-color:#334155;'>", unsafe_allow_html=True)
        
        # Switch back to User Mode
        if st.button("⬅️ Back to Legal Workspace", use_container_width=True):
            st.session_state.in_admin_mode = False
            st.rerun()

    return admin_tab