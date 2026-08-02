import streamlit as st
from datetime import datetime, timezone
from config.settings import PAGE_TITLE, MODES
from css.styles import load_css
from database.db import get_db, remaining_credits
from services.gemini_service import get_client
from components.onboarding import init_guest_session, render_bonus_banner
from components.sidebar import render_sidebar
from components.header import render_header
from components.chat import render_chat

# =====================================================================
# 1. PAGE CONFIG & STYLING
# =====================================================================
st.set_page_config(page_title=PAGE_TITLE, page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")
load_css()

# =====================================================================
# 2. SESSION STATE INIT
# =====================================================================
if "messages_by_mode" not in st.session_state:
    st.session_state.messages_by_mode = {m: [] for m in MODES}
if "history_titles" not in st.session_state:
    st.session_state.history_titles = []
if "last_request_ts" not in st.session_state:
    st.session_state.last_request_ts = 0.0
if "preset_prompt" not in st.session_state:
    st.session_state.preset_prompt = None

# Silently assigns every visitor a guest ID + free credits.
# No signup wall -- see components/onboarding.py.
init_guest_session()

# =====================================================================
# 3. SERVICES INIT
# =====================================================================
conn = get_db()
client = get_client()

if "has_logged_view" not in st.session_state:
    conn.execute("INSERT INTO page_views (timestamp) VALUES (?)", (datetime.now(timezone.utc).isoformat(),))
    conn.commit()
    st.session_state.has_logged_view = True

# =====================================================================
# 4. MAIN APPLICATION
# =====================================================================
user_id = st.session_state.user_id
credits_left = remaining_credits(conn, user_id)

app_mode = render_sidebar(conn, credits_left)

render_header(app_mode)
render_bonus_banner(conn)   # optional, dismissible +5 credit offer
render_chat(app_mode, conn, client, credits_left)