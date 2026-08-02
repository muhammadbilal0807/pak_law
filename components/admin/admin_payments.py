# components/admin/admin_payments.py (UPDATED)
import streamlit as st
import pandas as pd
from services.admin_service import log_audit_action
from database.db import add_credits

def render_admin_payments(conn):
    st.markdown('<div class="admin-header">Payments & Subscription Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="admin-subheader">Verify manual mobile wallet payments, approve credit top-ups, and review active pricing plans.</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["💳 Payment Approval Queue", "🏷️ Subscription Plans"])

    with tab1:
        df_payments = pd.read_sql_query("""
            SELECT p.id, u.email, p.gateway, p.trx_id, p.amount, p.credits_added, p.status, p.created_at 
            FROM payments p 
            LEFT JOIN accounts u ON p.account_id = u.id 
            ORDER BY p.created_at DESC
        """, conn)
        st.dataframe(df_payments, use_container_width=True, hide_index=True)
        
        st.markdown("### Approve Transaction")
        pending_trx = df_payments[df_payments["status"] == "Pending"] if not df_payments.empty else pd.DataFrame()
        
        if not pending_trx.empty:
            selected_pid = st.selectbox("Select Pending Payment ID", pending_trx["id"].tolist())
            if st.button("Approve Payment & Credit Account", type="primary"):
                trx_row = conn.execute("SELECT account_id, credits_added FROM payments WHERE id = ?", (selected_pid,)).fetchone()
                if trx_row:
                    uid, credits = trx_row[0], trx_row[1]
                    conn.execute("UPDATE payments SET status = 'Approved' WHERE id = ?", (selected_pid,))
                    # FIXED: Use add_credits function
                    add_credits(conn, uid, credits)
                    conn.commit()
                    log_audit_action(conn, st.session_state.user["id"], "APPROVE_PAYMENT", f"Approved payment {selected_pid} for user {uid}")
                    st.success(f"Payment approved and {credits} credits added.")
                    st.rerun()
        else:
            st.caption("No pending payment approvals.")

    with tab2:
        df_plans = pd.read_sql_query("SELECT * FROM subscription_plans", conn)
        st.dataframe(df_plans, use_container_width=True, hide_index=True)