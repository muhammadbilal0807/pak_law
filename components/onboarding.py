import streamlit as st
from config.settings import FREE_QUERY_LIMIT
from utils.validators import sanitize_user_id


def render_onboarding():
    """Renders the premium SaaS onboarding/login screen."""
    if not st.session_state.get("user_id"):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # IMPORTANT: this <div> is opened AND closed inside the same
            # st.markdown() call. Streamlit renders every st.markdown /
            # st.info / st.form call into its own isolated DOM node, so a
            # <div> left open here and "closed" later by a separate
            # st.markdown("</div>") call never actually wraps that later
            # content -- the browser silently auto-closes it right away.
            # That's why the card used to look broken: the form rendered
            # outside the styled box entirely.
            st.markdown("""
                <div class="onboarding-card animate-fade-in">
                    <div style="text-align: center;">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">⚖️</div>
                        <h2 style="font-weight: 700; color: #111827; margin-bottom: 0.5rem;">
                            Welcome to Pak Law AI
                        </h2>
                        <p style="color: #6B7280; font-size: 1rem; margin-bottom: 0;">
                            The definitive legal assistant for Pakistani law.
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.info(f"✨ Start with **{FREE_QUERY_LIMIT} free queries**. No credit card required.")

            with st.form("onboarding_form"):
                st.markdown("**Account Setup**")
                raw_id = st.text_input(
                    "Email or WhatsApp Number",
                    placeholder="e.g. you@company.com or 03xx-xxxxxxx",
                )
                submitted = st.form_submit_button(
                    "Continue to Workspace", type="primary", use_container_width=True
                )

            if submitted and raw_id.strip():
                sanitized = sanitize_user_id(raw_id)
                st.session_state.user_id = sanitized
                st.query_params["uid"] = sanitized
                st.rerun()

        st.stop()