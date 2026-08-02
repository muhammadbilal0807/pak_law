import streamlit as st

def render_header(app_mode):
    """Renders the top premium sticky navigation bar."""
    user_initial = "👤"
    if st.session_state.get("user_id"):
        user_id = st.session_state.user_id
        user_initial = user_id[0].upper() if user_id[0].isalpha() else "U"

    st.markdown(f"""
        <div class="top-nav animate-fade-in">
            <div class="nav-title">
                {app_mode} <span style="color:#94A3B8; font-weight:400; font-size:0.9rem;">| Pak Law AI Workspace</span>
            </div>
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="color: #64748B; cursor: pointer; transition: color 0.2s;" onmouseover="this.style.color='#0F172A'" onmouseout="this.style.color='#64748B'">🔔</div>
                <div class="nav-profile">{user_initial}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)