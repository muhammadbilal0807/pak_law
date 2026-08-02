import sqlite3
import pandas as pd
import uuid
import io

from datetime import datetime, timezone
from database.db import DB_FILE

def get_dashboard_metrics(conn):
    """Calculates key operational metrics for the Admin Dashboard."""
    metrics = {}
    
    # User Counts
    metrics["total_users"] = conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]
    metrics["active_users"] = conn.execute("SELECT COUNT(*) FROM accounts WHERE status = 'Active'").fetchone()[0]
    
    # Usage & Query Analytics
    metrics["total_queries"] = conn.execute("SELECT SUM(queries_used) FROM users").fetchone()[0] or 0
    metrics["total_chats"] = conn.execute("SELECT COUNT(*) FROM chats").fetchone()[0]
    metrics["total_messages"] = conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    metrics["total_tokens"] = conn.execute("SELECT SUM(tokens) FROM messages").fetchone()[0] or 0
    
    # Financials
    metrics["total_revenue"] = conn.execute("SELECT SUM(amount) FROM payments WHERE status = 'Approved'").fetchone()[0] or 0.0
    metrics["pending_payments"] = conn.execute("SELECT COUNT(*) FROM payments WHERE status = 'Pending'").fetchone()[0]
    
    # Database Knowledge
    metrics["laws_count"] = conn.execute("SELECT COUNT(*) FROM law_database").fetchone()[0]
    metrics["kb_chunks"] = conn.execute("SELECT COUNT(*) FROM knowledge_base").fetchone()[0]

    return metrics

def log_audit_action(conn, account_id, action, details="", ip_address="127.0.0.1"):
    """Inserts an irreversible security audit log into SQLite."""
    log_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    conn.execute("""
        INSERT INTO audit_logs (id, account_id, action, details, ip_address, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (log_id, account_id, action, details, ip_address, now))
    conn.commit()

def fetch_audit_logs(conn, limit=100):
    query = """
        SELECT a.timestamp, u.email, a.action, a.details, a.ip_address
        FROM audit_logs a
        LEFT JOIN accounts u ON a.account_id = u.id
        ORDER BY a.timestamp DESC LIMIT ?
    """
    return pd.read_sql_query(query, conn, params=(limit,))

def generate_database_backup(conn):
    """Generates an in-memory SQL dump for emergency system backups."""
    backup_db = io.StringIO()
    for line in conn.iterdump():
        backup_db.write(f'{line}\n')
    return backup_db.getvalue().encode('utf-8')