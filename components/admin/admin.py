# components/admin/admin.py (UPDATED)
import streamlit as st
from config.settings import UPGRADE_CREDITS
from utils.validators import sanitize_user_id
from database.db import get_all_users, add_credits

def render_admin_panel(conn):
    """Renders the admin panel inside the sidebar with minimalist styling."""
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("⚙️ Workspace Admin"):
        pw = st.text_input("Admin password", type="password", key="admin_pw")
        if pw and pw == st.secrets.get("ADMIN_PASSWORD", ""):
            total_views = conn.execute("SELECT COUNT(*) FROM page_views").fetchone()[0]
            st.metric(label="Total App Opens", value=total_views)
            
            st.divider()

            with st.form("add_credits_form"):
                st.markdown("**Top-up User**")
                target_id = st.text_input("User ID (as typed)")
                amount = st.number_input("Credits to add", min_value=1, value=UPGRADE_CREDITS, step=1)
                add_submit = st.form_submit_button("Add Credits", type="primary")
                
            if add_submit and target_id.strip():
                sanitized_target = sanitize_user_id(target_id)
                add_credits(conn, sanitized_target, int(amount))
                st.success(f"Added {amount} credits to {sanitized_target}")
                st.rerun()

            st.divider()
            st.markdown("**👁️ User Directory**")
            all_users = get_all_users(conn)
            if all_users:
                user_list = [
                    {
                        "User ID": row[0], 
                        "Joined": row[1][:10] if row[1] else "N/A", 
                        "Queries Used": row[2] if row[2] is not None else 0,
                        "Email": row[3] if len(row) > 3 else "N/A",
                        "Name": row[4] if len(row) > 4 else "N/A",
                        "Role": row[5] if len(row) > 5 else "User",
                        "Status": row[6] if len(row) > 6 else "Active"
                    } 
                    for row in all_users
                ]
                st.dataframe(user_list, use_container_width=True, hide_index=True)
            else:
                st.caption("No active users.")
        elif pw:
            st.error("Authentication failed.")