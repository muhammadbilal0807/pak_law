import streamlit as st

def load_css():
    """Loads all custom enterprise SaaS CSS styles for Pak Law AI."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* ---------------------------------------------------------
           1. GLOBAL & TYPOGRAPHY
        --------------------------------------------------------- */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            color: #1E293B;
        }
        
        /* Main background */
        .stApp {
            background-color: #F8FAFC !important;
        }

        /* Hide default header/footer */
        header { visibility: hidden !important; }
        footer { visibility: hidden !important; }
        
        /* Layout container width and padding */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 5rem !important;
            max-width: 900px !important;
        }

        /* ---------------------------------------------------------
           2. ANIMATIONS
        --------------------------------------------------------- */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
            animation: fadeIn 0.3s ease-out forwards;
        }

        /* ---------------------------------------------------------
           3. SIDEBAR & NAVIGATION
        --------------------------------------------------------- */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
            padding-top: 1rem;
        }
        
        .sidebar-logo {
            font-size: 1.25rem;
            font-weight: 700;
            color: #0F172A;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 1.5rem;
            padding-left: 10px;
            letter-spacing: -0.02em;
        }
        
        /* Premium Credit Card */
        .credit-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 16px;
            color: #1E293B;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            margin-bottom: 1rem;
        }
        .credit-title { font-size: 0.8rem; color: #64748B; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
        .credit-value { font-size: 1.5rem; font-weight: 700; margin: 4px 0; color: #0F172A; }
        
        /* Custom Progress bar */
        .stProgress > div > div > div > div {
            background-color: #0F172A !important;
            border-radius: 4px;
        }
        
        /* ---------------------------------------------------------
           4. BUTTONS & CARDS
        --------------------------------------------------------- */
        button[kind="primary"] {
            background-color: #0F172A !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 500 !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.2s ease !important;
        }
        button[kind="primary"]:hover {
            background-color: #334155 !important;
        }

        button[kind="secondary"] {
            background-color: #FFFFFF !important;
            color: #1E293B !important;
            border-radius: 8px !important;
            border: 1px solid #E2E8F0 !important;
            font-weight: 400 !important;
            padding: 0.5rem 1rem !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
            transition: all 0.2s ease !important;
        }
        button[kind="secondary"]:hover {
            border-color: #CBD5E1 !important;
            background-color: #F8FAFC !important;
        }

        /* Quick Prompt Cards */
        .prompt-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 16px;
            cursor: pointer;
            transition: all 0.2s ease;
            height: 100%;
        }
        .prompt-card:hover {
            border-color: #CBD5E1;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
            transform: translateY(-2px);
        }
        .prompt-card h4 {
            color: #0F172A;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 6px;
            margin-top: 0;
        }
        .prompt-card p {
            color: #64748B;
            font-size: 12px;
            line-height: 1.4;
            margin: 0;
        }

        /* ---------------------------------------------------------
           5. HERO & TOP NAV
        --------------------------------------------------------- */
        .top-nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem 0 1.5rem 0;
            border-bottom: 1px solid #E2E8F0;
            margin-bottom: 2rem;
        }
        .nav-title { font-size: 1.05rem; font-weight: 600; color: #0F172A; }
        .nav-profile {
            background-color: #F1F5F9;
            color: #0F172A;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 0.85rem;
            border: 1px solid #E2E8F0;
        }

        .hero-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #0F172A;
            text-align: center;
            margin-bottom: 0.4rem;
            letter-spacing: -0.03em;
        }
        .hero-subtitle {
            font-size: 1rem;
            color: #64748B;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 400;
        }

        /* ---------------------------------------------------------
           6. CHAT INTERFACE
        --------------------------------------------------------- */
        [data-testid="stChatInput"] {
            border-radius: 12px !important;
            border: 1px solid #CBD5E1 !important;
            box-shadow: 0 4px 20px -2px rgba(0,0,0,0.05) !important;
            background-color: #FFFFFF !important;
        }
        [data-testid="stChatInput"] textarea {
            font-size: 0.95rem !important;
            color: #1E293B !important;
        }
        [data-testid="stChatInput"]:focus-within {
            border-color: #0F172A !important;
            box-shadow: 0 0 0 2px rgba(15, 23, 42, 0.1) !important;
        }
        
        [data-testid="stChatMessage"] {
            padding: 1.25rem !important;
            border-radius: 12px !important;
            margin-bottom: 1rem !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.01) !important;
        }
        
        [data-testid="stChatMessage"][data-baseweb="card"]:nth-child(even) {
            background-color: #FFFFFF !important;
        }
        [data-testid="stChatMessage"]:nth-child(odd) {
            background-color: #FFFFFF !important;
        }

        .action-tray {
            display: flex;
            gap: 8px;
            margin-top: 8px;
            opacity: 0.7;
        }
        .action-tray:hover { opacity: 1; }

        /* ---------------------------------------------------------
           7. ONBOARDING & FORMS
        --------------------------------------------------------- */
        .onboarding-card {
            background: #FFFFFF;
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
            max-width: 460px;
            margin: 4rem auto;
            border: 1px solid #E2E8F0;
        }
        
        .stTextInput input, .stNumberInput input {
            border-radius: 8px !important;
            border: 1px solid #CBD5E1 !important;
            padding: 0.6rem 0.9rem !important;
            background-color: #FFFFFF !important;
        }
        .stTextInput input:focus {
            border-color: #0F172A !important;
            box-shadow: 0 0 0 2px rgba(15, 23, 42, 0.1) !important;
        }
        </style>
    """, unsafe_allow_html=True)