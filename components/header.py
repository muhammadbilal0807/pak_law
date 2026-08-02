import streamlit as st

def render_header():
    """Renders the main page header."""
    st.markdown("<div class='main-header'>⚖️ Pak Law AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Instant Legal Answers & Statute References for Pakistan</div>", unsafe_allow_html=True)