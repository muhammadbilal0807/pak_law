import streamlit as st
from config.settings import FREE_QUERY_LIMIT
from utils.validators import sanitize_user_id

def render_onboarding():
    """Renders the onboarding screen and blocks execution if user is not set."""
    if not st.session_state.get("user_id"):
        st.markdown("<div class='main-header'>⚖️ Pak Law AI</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-header'>Instant Legal Answers & Statute References for Pakistan</div>", unsafe_allow_html=True)
        st.info(f"You get **{FREE_QUERY_LIMIT} free questions**. Enter your WhatsApp number or email to start - "
                f"used only to track your free usage.")
        
        with st.form("onboarding_form"):
            raw_id = st.text_input("WhatsApp number or email", placeholder="03xx-xxxxxxx or you@email.com")
            submitted = st.form_submit_button("Start")
            
        if submitted and raw_id.strip():
            sanitized = sanitize_user_id(raw_id)
            st.session_state.user_id = sanitized
            st.query_params["uid"] = sanitized
            st.rerun()
            
        st.stop()