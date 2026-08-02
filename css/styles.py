import streamlit as st


def load_css():
    """Loads all custom CSS styles for the premium SaaS application."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* ---------------------------------------------------------
           1. GLOBAL & TYPOGRAPHY
           `color` now has !important. Without it, Streamlit's own
           theme-driven text color (light/white when a visitor's
           browser/OS prefers dark mode, or if they manually switch
           the in-app theme) was winning the cascade and making text
           invisible on our light backgrounds.
        --------------------------------------------------------- */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            color: #111827 !important;
        }

        .stApp {
            background-color: #F8FAFC !important;
        }

        header { visibility: hidden !important; }
        footer { visibility: hidden !important; }

        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 5rem !important;
            max-width: 1200px !important;
        }

        /* Safety net: force legible dark text on every normal
           markdown / label / expander element regardless of active
           theme. Scoped narrowly (stMarkdownContainer, labels,
           expander headers) so it never fights the intentionally
           LIGHT text set later for the credit card, hero accent,
           buttons, and chat bubbles. */
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3,
        [data-testid="stMarkdownContainer"] h4,
        [data-testid="stMarkdownContainer"] strong,
        [data-testid="stMarkdownContainer"] em,
        [data-testid="stWidgetLabel"] p,
        [data-testid="stExpander"] summary p,
        label {
            color: #111827 !important;
        }

        /* ---------------------------------------------------------
           1c. DISABLE STREAMLIT'S "STALE ELEMENT" FADE
           Streamlit automatically dims every on-screen element to a
           low opacity while a script rerun is in flight (that's the
           red/black progress bar you see at the very top of the
           page). This is normal Streamlit behaviour, but this app
           calls st.rerun() very frequently -- after every chat
           message, admin action, and login -- so users kept catching
           the app mid-fade, which looked like text randomly turning
           invisible. We force full opacity at all times so text
           stays legible through every rerun.
        --------------------------------------------------------- */
        [data-stale="true"],
        .element-container.stale-element,
        div[class*="stale-element"] {
            opacity: 1 !important;
            transition: none !important;
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
        [data-testid="stSidebar"] * {
            color: #111827;
        }

        .sidebar-logo {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0F766E !important;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 2rem;
            padding-left: 10px;
        }

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
        .credit-card * {
            color: #FFFFFF !important;
        }
        .credit-title { font-size: 0.9rem; opacity: 0.9; font-weight: 500; }
        .credit-value { font-size: 1.8rem; font-weight: 700; margin: 5px 0; }

        .stProgress > div > div > div > div {
            background-color: #10B981 !important;
            border-radius: 8px;
        }

        /* ---------------------------------------------------------
           4. BUTTONS & CARDS
        --------------------------------------------------------- */
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
        button[kind="primary"] p {
            color: #FFFFFF !important;
        }
        button[kind="primary"]:hover {
            background-color: #115E59 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 8px -1px rgba(15, 118, 110, 0.3) !important;
        }

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
        button[kind="secondary"] p {
            color: #111827 !important;
        }
        button[kind="secondary"]:hover {
            border-color: #0F766E !important;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05) !important;
            transform: translateY(-2px) !important;
            color: #0F766E !important;
        }
        button[kind="secondary"]:hover p {
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
        .hero-title span { color: #0F766E !important; }
        .hero-subtitle {
            font-size: 1.1rem;
            color: #6B7280;
            text-align: center;
            margin-bottom: 3rem;
        }

        /* ---------------------------------------------------------
           6. CHAT INTERFACE
        --------------------------------------------------------- */
        [data-testid="stChatInput"] {
            border-radius: 16px !important;
            border: 1px solid #E5E7EB !important;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05) !important;
            background-color: #FFFFFF !important;
            padding: 0.2rem !important;
        }
        [data-testid="stChatInput"] textarea {
            font-size: 1rem !important;
            color: #111827 !important;
        }

        [data-testid="stChatMessage"] {
            padding: 0.5rem 0 !important;
            margin-bottom: 0.5rem !important;
            animation: fadeIn 0.4s ease-out forwards;
            background: transparent !important;
            box-shadow: none !important;
            border: none !important;
        }

        /* Chat bubbles are colored via the stable `key=` class
           Streamlit attaches to st.container(key=...) -- e.g.
           key="bubble-user-legal-qa-0" becomes class
           "st-key-bubble-user-legal-qa-0". This is the reliable,
           version-proof way to color user vs assistant bubbles.
           (The old nth-child + data-baseweb="card" pair silently
           mismatched -- that attribute no longer exists on
           stChatMessage -- so the white-text rule fired without its
           matching teal-background rule, making every message
           invisible.) */
        div[class*="st-key-bubble-user"] {
            background-color: #0F766E !important;
            border-radius: 16px !important;
            border-bottom-right-radius: 4px !important;
            padding: 0.9rem 1.2rem !important;
            margin-left: 12% !important;
        }
        div[class*="st-key-bubble-user"] p,
        div[class*="st-key-bubble-user"] li,
        div[class*="st-key-bubble-user"] span,
        div[class*="st-key-bubble-user"] strong {
            color: #FFFFFF !important;
        }

        div[class*="st-key-bubble-assistant"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 16px !important;
            border-bottom-left-radius: 4px !important;
            padding: 0.9rem 1.2rem !important;
            margin-right: 12% !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02) !important;
        }
        div[class*="st-key-bubble-assistant"] p,
        div[class*="st-key-bubble-assistant"] li,
        div[class*="st-key-bubble-assistant"] span,
        div[class*="st-key-bubble-assistant"] strong {
            color: #111827 !important;
        }

        .action-tray {
            display: flex;
            gap: 10px;
            margin-top: 0.25rem;
            margin-bottom: 1.5rem;
            opacity: 0.7;
        }
        .action-tray:hover { opacity: 1; }

        /* ---------------------------------------------------------
           7. INPUTS & FORMS (Onboarding/Admin)
        --------------------------------------------------------- */
        .onboarding-card {
            background: #FFFFFF;
            padding: 2.5rem 2.5rem 1.5rem 2.5rem;
            border-radius: 24px;
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
            border: 1px solid #E5E7EB;
            max-width: 480px;
            margin: 3rem auto 1.5rem auto;
        }

        /* Streamlit's native st.form container -- used for the actual
           login inputs -- styled to look like part of the same card.
           Previously the form rendered OUTSIDE the .onboarding-card
           div entirely, because a raw <div> opened in one
           st.markdown() call can't wrap widgets from later, separate
           calls. */
        [data-testid="stForm"] {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 24px;
            padding: 2rem;
            max-width: 480px;
            margin: 0 auto;
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.06);
        }

        .stTextInput input, .stNumberInput input {
            border-radius: 12px !important;
            border: 1px solid #E5E7EB !important;
            padding: 0.8rem 1rem !important;
            background-color: #F9FAFB !important;
            color: #111827 !important;
            transition: all 0.2s ease !important;
        }
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: #0F766E !important;
            box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.2) !important;
        }

        /* ---------------------------------------------------------
           8. BONUS CREDITS BANNER (non-blocking)
        --------------------------------------------------------- */
        .bonus-card {
            background: linear-gradient(135deg, #FDE68A 0%, #FCD34D 100%);
            border-radius: 14px;
            padding: 14px 18px;
            margin-bottom: 0.75rem;
            border: 1px solid #F59E0B;
        }
        .bonus-card-text {
            color: #78350F !important;
            font-size: 0.95rem;
        }
        .bonus-card-text * { color: #78350F !important; }
        </style>
    """, unsafe_allow_html=True)