import sqlite3
import uuid
from datetime import datetime, timezone

def get_db():
    conn = sqlite3.connect("pak_law_ai.db", check_same_thread=False)
    create_tables(conn)
    return conn

def create_tables(conn):
    # Phase 1 & 2 Tables
    conn.execute("CREATE TABLE IF NOT EXISTS page_views (timestamp TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, joined_at TEXT, queries_used INTEGER)")
    
    # Phase 3: Expanded Tables
    conn.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE,
            password_hash TEXT,
            full_name TEXT,
            phone TEXT,
            role TEXT,
            created_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id TEXT PRIMARY KEY,
            account_id TEXT,
            title TEXT,
            mode TEXT,
            is_pinned INTEGER DEFAULT 0,
            is_archived INTEGER DEFAULT 0,
            created_at TEXT,
            updated_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            chat_id TEXT,
            role TEXT,
            content TEXT,
            tokens INTEGER,
            created_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookmarks (
            id TEXT PRIMARY KEY,
            account_id TEXT,
            message_id TEXT,
            note TEXT,
            created_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            account_id TEXT PRIMARY KEY,
            theme TEXT,
            language TEXT,
            notifications INTEGER
        )
    """)
    conn.commit()

# --- Legacy Credit System (Preserved) ---
def remaining_credits(conn, user_id):
    from config.settings import FREE_QUERY_LIMIT
    cursor = conn.execute("SELECT queries_used FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    used = row[0] if row else 0
    # Additional logic for paid credits can be attached here
    return FREE_QUERY_LIMIT - used

def spend_credit(conn, user_id, amount=1):
    cursor = conn.execute("SELECT queries_used FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        conn.execute("UPDATE users SET queries_used = queries_used + ? WHERE user_id = ?", (amount, user_id))
    else:
        conn.execute("INSERT INTO users (user_id, joined_at, queries_used) VALUES (?, ?, ?)", 
                     (user_id, datetime.now(timezone.utc).isoformat(), amount))
    conn.commit()

# --- Phase 3: Chat History & Bookmarks ---
def create_chat(conn, account_id, title, mode):
    chat_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    conn.execute("INSERT INTO chats (id, account_id, title, mode, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                 (chat_id, account_id, title, mode, now, now))
    conn.commit()
    return chat_id

def save_message(conn, chat_id, role, content, tokens=0):
    msg_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    conn.execute("INSERT INTO messages (id, chat_id, role, content, tokens, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                 (msg_id, chat_id, role, content, tokens, now))
    conn.execute("UPDATE chats SET updated_at = ? WHERE id = ?", (now, chat_id))
    conn.commit()
    return msg_id

def get_chats_for_user(conn, account_id):
    return conn.execute("SELECT id, title, mode, is_pinned FROM chats WHERE account_id = ? AND is_archived = 0 ORDER BY is_pinned DESC, updated_at DESC", (account_id,)).fetchall()

def get_messages_for_chat(conn, chat_id):
    return conn.execute("SELECT id, role, content, created_at FROM messages WHERE chat_id = ? ORDER BY created_at ASC", (chat_id,)).fetchall()