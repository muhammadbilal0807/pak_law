import streamlit as st
from services.admin_service import fetch_audit_logs, generate_database_backup

def render_admin_system(conn):
    st.markdown('<div class="admin-header">System Health & Security Audit Logs</div>', unsafe_allow_html=True)
    st.markdown('<div class="admin-subheader">Review security audit logs, maintain access records, and download encrypted database backups.</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🛡️ Audit Trail Logs", "💾 Database Backup & Restore"])

    with tab1:
        st.markdown("### Security Audit Trail")
        df_logs = fetch_audit_logs(conn, limit=100)
        st.dataframe(df_logs, use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("### System Backup")
        st.write("Click below to download a full SQL dump of the production database.")
        backup_bytes = generate_database_backup(conn)
        st.download_button("📥 Download SQLite Database Dump (.sql)", backup_bytes, file_name="pak_law_ai_backup.sql", mime="text/plain")