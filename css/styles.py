import streamlit as st

def load_css():
    """Loads all custom CSS styles for the premium SaaS application."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* ---------------------------------------------------------
           1. GLOBAL & TYPOGRAPHY
        --------------------------------------------------------- */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            color: #0F172A;
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
            padding-top: 2rem !important;
            padding-bottom: 5rem !important;
            max-width: 1000px !important; /* Slightly narrower for better reading experience */
        }

        /* ---------------------------------------------------------
           2. ANIMATIONS
        --------------------------------------------------------- */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
            animation: fadeIn 0.4s ease-out forwards;
        }

        /* ---------------------------------------------------------
           3. SIDEBAR & NAVIGATION
        --------------------------------------------------------- */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
        }
        
        /* Sidebar Logo Area */
        .sidebar-logo {
            font-size: 1.4rem;
            font-weight: 700;
            color: #0F766E;
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 2rem;
            padding: 10px 15px;
            letter-spacing: -0.5px;
        }
        
        /* Premium Credit Card */
        .credit-card {
            background: linear-gradient(135deg, #0F766E 0%, #115E59 100%);
            border-radius: 12px;
            padding: 24px;
            color: #FFFFFF;
            box-shadow: 0 4px 14px 0 rgba(15, 118, 110, 0.25);
            margin: 0 10px 1.5rem 10px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .credit-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(15, 118, 110, 0.3);
        }
        .credit-title { font-size: 0.85rem; opacity: 0.85; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;}
        .credit-value { font-size: 2.2rem; font-weight: 700; margin: 4px 0; }
        
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
            border-radius: 8px !important;
            border: none !important;
            font-weight: 500 !important;
            padding: 0.6rem 1.2rem !important;
            transition: all 0.2s ease !important;
        }
        button[kind="primary"]:hover {
            background-color: #115E59 !important;
            box-shadow: 0 4px 12px rgba(15, 118, 110, 0.2) !important;
        }

        /* Secondary Buttons / Quick Action Cards */
        button[kind="secondary"] {
            background-color: #FFFFFF !important;
            color: #1E293B !important;
            border-radius: 12px !important;
            border: 1px solid #E2E8F0 !important;
            font-weight: 400 !important;
            padding: 1.2rem !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
            text-align: left !important;
        }
        button[kind="secondary"]:hover {
            border-color: #0F766E !important;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05) !important;
            transform: translateY(-2px) !important;
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
        .nav-title { font-size: 1.1rem; font-weight: 600; color: #0F172A; }
        .nav-profile {
            background-color: #CCFBF1;
            color: #0F766E;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 0.9rem;
        }

        .hero-title {
            font-size: 2.8rem;
            font-weight: 700;
            color: #0F172A;
            text-align: center;
            margin-bottom: 0.5rem;
            letter-spacing: -0.03em;
        }
        .hero-title span { color: #0F766E; }
        .hero-subtitle {
            font-size: 1.1rem;
            color: #64748B;
            text-align: center;
            margin-bottom: 3rem;
            font-weight: 300;
        }

        /* ---------------------------------------------------------
           6. CHAT INTERFACE
        --------------------------------------------------------- */
        /* Chat Input Container */
        [data-testid="stChatInput"] {
            border-radius: 12px !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 4px 20px -2px rgba(0,0,0,0.05) !important;
            background-color: #FFFFFF !important;
        }
        
        /* Chat Bubbles */
        [data-testid="stChatMessage"] {
            padding: 1.5rem !important;
            border-radius: 12px !important;
            margin-bottom: 1.5rem !important;
            animation: fadeIn 0.4s ease-out forwards;
        }
        
        /* User Message */
        [data-testid="stChatMessage"][data-baseweb="card"]:nth-child(even) {
            background-color: #F1F5F9 !important;
            border: 1px solid #E2E8F0 !important;
            margin-left: 3rem !important;
            border-bottom-right-radius: 4px !important;
        }
        
        /* Assistant Message */
        [data-testid="stChatMessage"]:nth-child(odd) {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
            margin-right: 3rem !important;
            border-bottom-left-radius: 4px !important;
        }

        /* Action Buttons underneath assistant */
        .action-tray {
            display: flex;
            gap: 12px;
            margin-top: 10px;
            opacity: 0;
            transition: opacity 0.2s ease;
        }
        [data-testid="stChatMessage"]:hover .action-tray { opacity: 1; }
        
        .action-tray button {
            background: #F1F5F9;
            border: none;
            border-radius: 6px;
            padding: 6px 10px;
            cursor: pointer;
            color: #64748B;
            transition: background 0.2s ease, color 0.2s ease;
            font-size: 0.9rem;
        }
        .action-tray button:hover {
            background: #E2E8F0;
            color: #0F172A;
        }

        /* ---------------------------------------------------------
           7. INPUTS & FORMS (Onboarding/Admin)
        --------------------------------------------------------- */
        .onboarding-card {
            background: #FFFFFF;
            padding: 3.5rem 3rem;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05), 0 8px 10px -6px rgba(0,0,0,0.01);
            max-width: 480px;
            margin: 4rem auto;
            border: 1px solid #E2E8F0;
        }
        
        .stTextInput input, .stNumberInput input {
            border-radius: 8px !important;
            border: 1px solid #CBD5E1 !important;
            padding: 0.7rem 1rem !important;
            background-color: #FFFFFF !important;
            transition: all 0.2s ease !important;
        }
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: #0F766E !important;
            box-shadow: 0 0 0 2px rgba(15, 118, 110, 0.15) !important;
        }
        </style>
    """, unsafe_allow_html=True)