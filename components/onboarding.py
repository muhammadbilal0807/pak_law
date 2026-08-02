import streamlit as st
from services.auth_service import authenticate_user, register_user

def render_onboarding(conn):
    if "user" not in st.session_state:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
                <div class="onboarding-card animate-fade-in">
                    <div style="text-align: center; margin-bottom: 2rem;">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">⚖️</div>
                        <h2 style="font-weight: 700; color: #111827; margin-bottom: 0.5rem;">Pak Law AI</h2>
                        <p style="color: #6B7280; font-size: 1rem;">Your Complete Legal AI Assistant.</p>
                    </div>
            """, unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["Login", "Register"])
            
            with tab1:
                with st.form("login_form"):
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    if st.form_submit_button("Login", type="primary", use_container_width=True):
                        success, result = authenticate_user(conn, email, password)
                        if success:
                            st.session_state.user = result
                            st.session_state.user_id = result["id"] # Legacy support
                            st.rerun()
                        else:
                            st.error(result)
                            
            with tab2:
                with st.form("register_form"):
                    new_name = st.text_input("Full Name")
                    new_email = st.text_input("Email")
                    new_password = st.text_input("Password", type="password")
                    if st.form_submit_button("Create Account", type="primary", use_container_width=True):
                        success, result = register_user(conn, new_email, new_password, new_name)
                        if success:
                            st.success("Account created! Please log in.")
                        else:
                            st.error(result)

            st.markdown("</div>", unsafe_allow_html=True)
        st.stop()