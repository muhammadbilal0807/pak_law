import streamlit as st
from datetime import datetime, timezone

from config.settings import PAGE_TITLE, MODES, ADMIN_ROLES
from css.styles import load_css
from css.admin_styles import load_admin_css
from database.db import get_db, remaining_credits
from services.gemini_service import get_client

from components.onboarding import render_onboarding
from components.sidebar import render_sidebar
from components.header import render_header
from components.chat import render_chat
from components.profile import render_profile

# Admin Suite Components
from components.admin.admin_sidebar import render_admin_sidebar
from components.admin.admin_dashboard import render_admin_dashboard
from components.admin.admin_user_mgmt import render_admin_user_mgmt
from components.admin.admin_law_kb import render_admin_law_kb
from components.admin.admin_prompts_ai import render_admin_prompts_ai
from components.admin.admin_analytics import render_admin_analytics
from components.admin.admin_payments import render_admin_payments
from components.admin.admin_system import render_admin_system

# 1. PAGE CONFIG
st.set_page_config(page_title=PAGE_TITLE, page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

# 2. SESSION INIT
if "messages_by_mode" not in st.session_state:
    st.session_state.messages_by_mode = {m: [] for m in MODES}
if "history_titles" not in st.session_state:
    st.session_state.history_titles = []
if "in_admin_mode" not in st.session_state:
    st.session_state.in_admin_mode = False

# 3. DB & AI CLIENT INIT
conn = get_db()
client = get_client()

# Page View Tracker
if "has_logged_view" not in st.session_state:
    conn.execute("INSERT INTO page_views (timestamp) VALUES (?)", (datetime.now(timezone.utc).isoformat(),))
    conn.commit()
    st.session_state.has_logged_view = True

# 4. AUTHENTICATION GATEWAY
render_onboarding(conn)

user = st.session_state.user
user_role = user.get("role", "User")
credits_left = remaining_credits(conn, user["id"])

# 5. ADMIN MODE vs USER WORKSPACE ROUTING
# Allow toggle to admin workspace if user possesses Admin or Super Admin role
if user_role in ADMIN_ROLES:
    with st.sidebar:
        if not st.session_state.in_admin_mode:
            if st.button("⚡ Open Admin Workspace", type="primary", use_container_width=True):
                st.session_state.in_admin_mode = True
                st.rerun()

if st.session_state.in_admin_mode and user_role in ADMIN_ROLES:
    # --- ADMIN WORKSPACE ---
    load_admin_css()
    admin_tab = render_admin_sidebar()
    
    if admin_tab == "Overview":
        render_admin_dashboard(conn)
    elif admin_tab == "User Control":
        render_admin_user_mgmt(conn)
    elif admin_tab == "Law Database":
        render_admin_law_kb(conn, is_kb_mode=False)
    elif admin_tab == "Knowledge Base":
        render_admin_law_kb(conn, is_kb_mode=True)
    elif admin_tab == "Prompts & AI Config":
        render_admin_prompts_ai(conn)
    elif admin_tab == "Analytics":
        render_admin_analytics(conn)
    elif admin_tab == "Payments & Plans":
        render_admin_payments(conn)
    elif admin_tab == "System & Security":
        render_admin_system(conn)
    else:
        st.info("Module loading...")
else:
    # --- STANDARD USER WORKSPACE ---
    load_css()
    app_mode = render_sidebar(conn, credits_left)
    render_header(app_mode)

    if app_mode in ["Legal Q&A", "Drafting", "Analysis"]:
        render_chat(app_mode, conn, client, credits_left)
    elif app_mode == "Profile":
        render_profile(conn, credits_left)
    elif app_mode == "Bookmarks":
        st.info("🔖 Bookmarks system connected to SQLite database.")
    elif app_mode == "Settings":
        st.info("⚙️ Settings: Configure preferences, theme, and data exports.")
# app.py (UPDATED - add import and handle conversation tab)
# Add this import at the top:
from components.admin.admin_conversations import render_admin_conversations

# In the admin routing section, add:
elif admin_tab == "Conversations":
    render_admin_conversations(conn)