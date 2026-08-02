# css/styles.py
import streamlit as st

def load_css():
    """Load custom CSS for the user workspace"""
    st.markdown("""
    <style>
        /* Main Container */
        .main {
            padding: 0 1rem;
        }
        
        /* Sidebar */
        .sidebar-logo {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0F766E;
            padding: 0.5rem 0;
            margin-bottom: 1rem;
            border-bottom: 2px solid #E5E7EB;
        }
        
        /* Credit Card */
        .credit-card {
            background: linear-gradient(135deg, #0F766E 0%, #115E59 100%);
            border-radius: 12px;
            padding: 1.5rem;
            color: white;
            margin: 1rem 0;
        }
        
        .credit-title {
            font-size: 0.85rem;
            opacity: 0.9;
            font-weight: 500;
        }
        
        .credit-value {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0.25rem 0;
        }
        
        /* Top Navigation */
        .top-nav {
            background: white;
            padding: 1rem 2rem;
            border-bottom: 1px solid #E5E7EB;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
        }
        
        .nav-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #111827;
        }
        
        .nav-profile {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: #E0F2FE;
            color: #0369A1;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            cursor: pointer;
        }
        
        /* Onboarding Card */
        .onboarding-card {
            background: white;
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
            margin: 2rem 0;
        }
        
        /* Animations */
        .animate-fade-in {
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Custom Button Styles */
        .stButton button {
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }
        
        /* Chat Message Styles */
        .stChatMessage {
            border-radius: 12px;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)