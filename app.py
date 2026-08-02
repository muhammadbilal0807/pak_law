import streamlit as st
from css.styles import load_css
from database.db import get_db, remaining_credits
from services.gemini_service import get_client

from components.onboarding import render_onboarding
from components.sidebar import render_sidebar
from components.header import render_header
from components.chat import render_chat
from components.profile import render_profile

# 1. PAGE CONFIG
st.set_page_config(page_title="Pak Law AI Workspace", page_icon="⚖️", layout="wide")
load_css()

# 2. INIT
conn = get_db()
client = get_client()

# 3. AUTH WALL
render_onboarding(conn)

# 4. WORKSPACE
user_id = st.session_state.user["id"]
credits_left = remaining_credits(conn, user_id)

app_mode = render_sidebar(conn, credits_left)
render_header(app_mode)

# 5. ROUTING
if app_mode in ["Legal Q&A", "Drafting", "Analysis"]:
    render_chat(app_mode, conn, client, credits_left)
elif app_mode == "Profile":
    render_profile(conn, credits_left)
elif app_mode == "Bookmarks":
    st.info("🔖 Bookmarks system connected to SQLite. Select a bookmark from the list to view.")
elif app_mode == "Settings":
    st.info("⚙️ Workspace Settings: Configure Theme, Notifications, and Export formats here.")