import streamlit as st
from services.auth_service import logout

def render_profile(conn, credits_left):
    user = st.session_state.user
    
    st.markdown("<h2 style='color:#111827; margin-bottom: 2rem;'>👤 Profile & Account</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
            <div style="background: white; padding: 2rem; border-radius: 12px; border: 1px solid #E5E7EB; margin-bottom: 1rem;">
                <h3 style="margin-top:0;">{user['full_name']}</h3>
                <p style="color:#6B7280;">{user['email']}</p>
                <div style="margin-top: 1rem;">
                    <span style="background:#E0F2FE; color:#0369A1; padding:4px 12px; border-radius:12px; font-size:0.85rem; font-weight:600;">
                        Role: {user['role']}
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🔒 Security & Password"):
            st.text_input("Current Password", type="password")
            st.text_input("New Password", type="password")
            st.button("Update Password", type="primary")

    with col2:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0F766E 0%, #115E59 100%); padding: 2rem; border-radius: 12px; color: white;">
                <h4 style="margin-top:0; opacity: 0.9;">Plan: Free Tier</h4>
                <h1 style="margin: 1rem 0; font-size: 3rem;">{credits_left}</h1>
                <p style="opacity: 0.9; font-size: 0.9rem;">Credits Remaining</p>
                <button style="background: white; color: #0F766E; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600; width: 100%; margin-top: 1rem;">
                    Upgrade Plan
                </button>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()