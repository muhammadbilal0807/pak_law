import streamlit as st
from config.settings import FREE_QUERY_LIMIT
from utils.validators import sanitize_user_id

def render_onboarding():
    """Renders the SaaS onboarding/login screen with polished light theme."""
    if not st.session_state.get("user_id"):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
                <div class="onboarding-card animate-fade-in">
                    <div style="text-align: center; margin-bottom: 2rem;">
                        <div style="font-size: 3rem; margin-bottom: 0.75rem;">⚖️</div>
                        <h2 style="font-weight: 700; color: #0F172A; margin-bottom: 0.4rem; font-size: 1.5rem;">Welcome to Pak Law AI</h2>
                        <p style="color: #64748B; font-size: 0.95rem;">
                            Enterprise legal intelligence for Pakistani law.
                        </p>
                    </div>
            """, unsafe_allow_html=True)
            
            st.info(f"✨ Start with **{FREE_QUERY_LIMIT} free queries**. No credit card required.")
            
            with st.form("onboarding_form"):
                st.markdown("<p style='font-weight: 500; color: #334155; margin-bottom: 4px; font-size:0.9rem;'>Account Setup</p>", unsafe_allow_html=True)
                raw_id = st.text_input("Email or WhatsApp Number", placeholder="e.g. you@company.com or 03xx-xxxxxxx", label_visibility="collapsed")
                st.markdown("<br>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Continue to Workspace", type="primary", use_container_width=True)
                
            if submitted and raw_id.strip():
                sanitized = sanitize_user_id(raw_id)
                st.session_state.user_id = sanitized
                st.query_params["uid"] = sanitized
                st.rerun()
                
            st.markdown("</div>", unsafe_allow_html=True)
        st.stop()