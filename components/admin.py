import streamlit as st
from config.settings import UPGRADE_CREDITS
from utils.validators import sanitize_user_id
from database.db import get_all_users, add_credits

def render_admin_panel(conn):
    """Renders the admin panel inside the sidebar."""
    with st.expander("🔐 Admin"):
        pw = st.text_input("Admin password", type="password", key="admin_pw")
        if pw and pw == st.secrets.get("ADMIN_PASSWORD", ""):
            total_views = conn.execute("SELECT COUNT(*) FROM page_views").fetchone()[0]
            st.metric(label="Total App Opens", value=total_views)
            
            st.divider()

            with st.form("add_credits_form"):
                target_id = st.text_input("User ID (as they typed it)")
                amount = st.number_input("Credits to add", min_value=1, value=UPGRADE_CREDITS, step=1)
                add_submit = st.form_submit_button("Add Credits")
                
            if add_submit and target_id.strip():
                sanitized_target = sanitize_user_id(target_id)
                add_credits(conn, sanitized_target, int(amount))
                st.success(f"Added {amount} credits to {sanitized_target}")

            st.divider()
            st.markdown("### 👁️ Registered Viewers")
            all_users = get_all_users(conn)
            if all_users:
                user_list = [
                    {
                        "User ID": row[0], 
                        "Joined Date": row[1][:10], 
                        "Queries Ran": row[2]
                    } 
                    for row in all_users
                ]
                st.dataframe(user_list, use_container_width=True)
            else:
                st.caption("No users have registered yet.")

        elif pw:
            st.error("Wrong password")