import streamlit as st

def load_css():
    """Loads all custom CSS styles for the application."""
    st.markdown("""
        <style>
        .main-header { font-size: 2.2rem; font-weight: 700; text-align: center; margin-bottom: 0.2rem; }
        .sub-header { font-size: 1.0rem; color: #888888; text-align: center; margin-bottom: 1.5rem; }
        .paywall-box { border: 2px solid #ff4b4b; padding: 20px; border-radius: 10px; text-align: center; background-color: #fff0f0; color: #900; }
        div.stButton > button { width: 100%; border-radius: 8px; text-align: left; padding: 0.5rem 0.8rem; }
        </style>
    """, unsafe_allow_html=True)