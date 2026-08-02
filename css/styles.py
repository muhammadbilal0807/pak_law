import streamlit as st

def load_css():
    """Loads all custom CSS styles for the premium SaaS application."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* ---------------------------------------------------------
           1. GLOBAL & TYPOGRAPHY
        --------------------------------------------------------- */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            color: #111827;
        }
        
        /* Main background */
        .stApp {
            background-color: #F8FAFC !important;
        }

        /* Hide default header/footer */
        header { visibility: hidden !important; }
        footer { visibility: hidden !important; }
        
        /* Top padding reduction */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 5rem !important;
            max-width: 1200px !important;
        }

        /* ---------------------------------------------------------
           2. ANIMATIONS
        --------------------------------------------------------- */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
            animation: fadeIn 0.5s ease-out forwards;
        }

        /* ---------------------------------------------------------
           3. SIDEBAR & NAVIGATION
        --------------------------------------------------------- */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E5E7EB !important;
            padding-top: 1rem;
        }
        
        /* Sidebar Logo Area */
        .sidebar-logo {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0F766E;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 2rem;
            padding-left: 10px;
        }
        
        /* Premium Credit Card */
        .credit-card {
            background: linear-gradient(135deg, #0F766E 0%, #115E59 100%);
            border-radius: 16px;
            padding: 20px;
            color: #FFFFFF;
            box-shadow: 0 10px 15px -3px rgba(15, 118, 110, 0.3);
            margin-bottom: 1.5rem;
            transition: transform 0.2s ease;
        }
        .credit-card:hover {
            transform: translateY(-2px);
        }
        .credit-title { font-size: 0.9rem; opacity: 0.9; font-weight: 500; }
        .credit-value { font-size: 1.8rem; font-weight: 700; margin: 5px 0; }
        
        /* Custom Progress bar */
        .stProgress > div > div > div > div {
            background-color: #10B981 !important;
            border-radius: 8px;
        }
        
        /* ---------------------------------------------------------
           4. BUTTONS & CARDS
        --------------------------------------------------------- */
        /* Primary Buttons */
        button[kind="primary"] {
            background-color: #0F766E !important;
            color: #FFFFFF !important;
            border-radius: 12px !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 0.5rem 1rem !important;
            box-shadow: 0 4px 6px -1px rgba(15, 118, 110, 0.2) !important;
            transition: all 0.2s ease !important;
        }
        button[kind="primary"]:hover {
            background-color: #115E59 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 8px -1px rgba(15, 118, 110, 0.3) !important;
        }

        /* Secondary Buttons / Quick Action Cards */
        button[kind="secondary"] {
            background-color: #FFFFFF !important;
            color: #111827 !important;
            border-radius: 16px !important;
            border: 1px solid #E5E7EB !important;
            font-weight: 500 !important;
            padding: 1.2rem !important;
            box-shadow: 0 2px 4px -1px rgba(0,0,0,0.03) !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
            text-align: left !important;
            display: flex;
            align-items: flex-start;
            justify-content: flex-start;
            height: 100%;
        }
        button[kind="secondary"]:hover {
            border-color: #0F766E !important;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05) !important;
            transform: translateY(-2px) !important;
            color: #0F766E !important;
        }

        /* ---------------------------------------------------------
           5. HERO & TOP NAV
        --------------------------------------------------------- */
        .top-nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0 2rem 0;
            border-bottom: 1px solid #E5E7EB;
            margin-bottom: 2rem;
        }
        .nav-title { font-size: 1.2rem; font-weight: 600; color: #111827; }
        .nav-profile {
            background-color: #D1FAE5;
            color: #0F766E;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
        }

        .hero-title {
            font-size: 3rem;
            font-weight: 700;
            color: #111827;
            text-align: center;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }
        .hero-title span { color: #0F766E; }
        .hero-subtitle {
            font-size: 1.1rem;
            color: #6B7280;
            text-align: center;
            margin-bottom: 3rem;
        }

        /* ---------------------------------------------------------
           6. CHAT INTERFACE
        --------------------------------------------------------- */
        /* Chat Input Container */
        [data-testid="stChatInput"] {
            border-radius: 16px !important;
            border: 1px solid #E5E7EB !important;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05) !important;
            background-color: #FFFFFF !important;
            padding: 0.2rem !important;
        }
        [data-testid="stChatInput"] textarea {
            font-size: 1rem !important;
        }
        
        /* Chat Bubbles */
        [data-testid="stChatMessage"] {
            padding: 1.5rem !important;
            border-radius: 16px !important;
            margin-bottom: 1rem !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02) !important;
            animation: fadeIn 0.4s ease-out forwards;
        }
        
        /* User Message */
        [data-testid="stChatMessage"][data-baseweb="card"]:nth-child(even) {
            background-color: #0F766E !important;
            color: #FFFFFF !important;
            margin-left: 2rem !important;
            border-bottom-right-radius: 4px !important;
        }
        [data-testid="stChatMessage"]:nth-child(even) [data-testid="stMarkdownContainer"] p {
            color: #FFFFFF !important;
        }
        
        /* Assistant Message */
        [data-testid="stChatMessage"]:nth-child(odd) {
            background-color: #FFFFFF !important;
            border: 1px solid #E5E7EB !important;
            margin-right: 2rem !important;
            border-bottom-left-radius: 4px !important;
        }

        /* Action Buttons underneath assistant */
        .action-tray {
            display: flex;
            gap: 10px;
            margin-top: -0.5rem;
            margin-bottom: 2rem;
            opacity: 0.7;
        }
        .action-tray:hover { opacity: 1; }

        /* ---------------------------------------------------------
           7. INPUTS & FORMS (Onboarding/Admin)
        --------------------------------------------------------- */
        .onboarding-card {
            background: #FFFFFF;
            padding: 3rem;
            border-radius: 24px;
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
            max-width: 500px;
            margin: 4rem auto;
            border: 1px solid #E5E7EB;
        }
        
        .stTextInput input, .stNumberInput input {
            border-radius: 12px !important;
            border: 1px solid #E5E7EB !important;
            padding: 0.8rem 1rem !important;
            background-color: #F9FAFB !important;
            transition: all 0.2s ease !important;
        }
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: #0F766E !important;
            box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.2) !important;
        }
        </style>
    """, unsafe_allow_html=True)