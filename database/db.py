import sqlite3
from datetime import datetime, timezone
import streamlit as st
from config.settings import DB_PATH, FREE_QUERY_LIMIT

@st.cache_resource
def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            credits_used INTEGER DEFAULT 0,
            credits_purchased INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS page_views (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT
        )
    """)
    conn.commit()
    return conn

def _get_or_create_user(conn, user_id):
    row = conn.execute("SELECT credits_used, credits_purchased FROM users WHERE user_id=?", (user_id,)).fetchone()
    if row is None:
        conn.execute(
            "INSERT INTO users (user_id, credits_used, credits_purchased, created_at) VALUES (?, 0, 0, ?)",
            (user_id, datetime.now(timezone.utc).isoformat())
        )
        conn.commit()
        return 0, 0
    return row

def remaining_credits(conn, user_id):
    used, purchased = _get_or_create_user(conn, user_id)
    return FREE_QUERY_LIMIT + purchased - used

def spend_credit(conn, user_id, amount=1):
    _get_or_create_user(conn, user_id)
    conn.execute("UPDATE users SET credits_used = credits_used + ? WHERE user_id=?", (amount, user_id))
    conn.commit()

def add_credits(conn, user_id, amount):
    _get_or_create_user(conn, user_id)
    conn.execute("UPDATE users SET credits_purchased = credits_purchased + ? WHERE user_id=?", (amount, user_id))
    conn.commit()

def get_all_users(conn):
    return conn.execute("SELECT user_id, created_at, credits_used FROM users ORDER BY created_at DESC").fetchall()