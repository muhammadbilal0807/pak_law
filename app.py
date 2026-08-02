import streamlit as st
from datetime import datetime, timezone

from config.settings import PAGE_TITLE, MODES
from css.styles import load_css
from database.db import get_db, remaining_credits
from services.gemini_service import get_client

from components.onboarding import render_onboarding
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
if "user_id" not in st.session_state:
    st.session_state.user_id = st.query_params.get("uid")
if "last_request_ts" not in st.session_state:
    st.session_state.last_request_ts = 0.0
if "preset_prompt" not in st.session_state:
    st.session_state.preset_prompt = None

# =====================================================================
# 3. SERVICES INIT
# =====================================================================
conn = get_db()
client = get_client()

# Log a page view once per browser session
if "has_logged_view" not in st.session_state:
    conn.execute("INSERT INTO page_views (timestamp) VALUES (?)", (datetime.now(timezone.utc).isoformat(),))
    conn.commit()
    st.session_state.has_logged_view = True

# =====================================================================
# 4. ONBOARDING
# =====================================================================
# Will halt execution if user is not authenticated, presenting the sleek SaaS login card.
render_onboarding()

# =====================================================================
# 5. MAIN APPLICATION
# =====================================================================
user_id = st.session_state.user_id
credits_left = remaining_credits(conn, user_id)

# Render premium sidebar
app_mode = render_sidebar(conn, credits_left)

# Render main workspace
render_header(app_mode)
render_chat(app_mode, conn, client, credits_left)