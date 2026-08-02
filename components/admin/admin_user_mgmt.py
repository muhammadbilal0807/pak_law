# components/admin/admin_user_mgmt.py (UPDATED)
import streamlit as st
import pandas as pd
from services.admin_service import log_audit_action
from database.db import add_credits, get_user_credits

def render_admin_user_mgmt(conn):
    st.markdown('<div class="admin-header">User & Role Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="admin-subheader">View registered users, assign administrative roles, suspend accounts, and manage credits.</div>', unsafe_allow_html=True)

    # Search bar & Filters
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search_term = st.text_input("🔍 Search users by email or name...", key="user_search")
    with col_filter:
        role_filter = st.selectbox("Role Filter", ["All", "User", "Moderator", "Admin", "Super Admin"])

    # Query Users
    query = "SELECT id, full_name, email, role, status, created_at FROM accounts"
    df_users = pd.read_sql_query(query, conn)
    
    if search_term:
        df_users = df_users[df_users['email'].str.contains(search_term, case=False, na=False) | 
                            df_users['full_name'].str.contains(search_term, case=False, na=False)]
    if role_filter != "All":
        df_users = df_users[df_users['role'] == role_filter]

    st.dataframe(df_users, use_container_width=True, hide_index=True)

    st.divider()

    # User Modification Form
    st.markdown("### ⚙️ Account Actions")
    col_u1, col_u2 = st.columns(2)
    
    with col_u1:
        st.markdown("**Role & Status Assignment**")
        selected_email = st.selectbox("Select User Email", df_users['email'].tolist() if not df_users.empty else [])
        if selected_email:
            new_role = st.selectbox("Assign New Role", ["User", "Moderator", "Admin", "Super Admin"])
            new_status = st.selectbox("Account Status", ["Active", "Suspended"])
            
            if st.button("Save User Changes", type="primary"):
                conn.execute("UPDATE accounts SET role = ?, status = ? WHERE email = ?", (new_role, new_status, selected_email))
                conn.commit()
                log_audit_action(conn, st.session_state.user["id"], "UPDATE_USER", f"Updated {selected_email} to {new_role}/{new_status}")
                st.success(f"Updated {selected_email} successfully.")
                st.rerun()

    with col_u2:
        st.markdown("**Manual Credit Top-up**")
        if selected_email:
            user_row = conn.execute("SELECT id FROM accounts WHERE email = ?", (selected_email,)).fetchone()
            if user_row:
                uid = user_row[0]
                current_credits = get_user_credits(conn, uid)
                st.info(f"Current Credits: {current_credits}")
                credits_to_add = st.number_input("Credits to Add", min_value=1, value=50, step=5)
                if st.button("Add Credits", type="primary"):
                    add_credits(conn, uid, credits_to_add)
                    log_audit_action(conn, st.session_state.user["id"], "TOPUP_CREDITS", f"Added {credits_to_add} credits to {selected_email}")
                    st.success(f"Added {credits_to_add} credits to {selected_email}")
                    st.rerun()