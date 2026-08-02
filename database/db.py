# database/db.py (UPDATED)
import sqlite3
import uuid
from datetime import datetime, timezone

DB_FILE = "pak_law_ai.db"

def get_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    create_tables(conn)
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    
    # Legacy & Base Tables
    cursor.execute("CREATE TABLE IF NOT EXISTS page_views (timestamp TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, joined_at TEXT, queries_used INTEGER)")
    
    # Phase 3 Accounts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE,
            password_hash TEXT,
            full_name TEXT,
            phone TEXT,
            role TEXT DEFAULT 'User',
            status TEXT DEFAULT 'Active',
            created_at TEXT,
            last_login TEXT
        )
    """)
    
    # User Settings Table (FIXED: Added missing table)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            account_id TEXT PRIMARY KEY,
            theme TEXT DEFAULT 'Light',
            language TEXT DEFAULT 'English',
            notifications INTEGER DEFAULT 1,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )
    """)
    
    # Phase 4 Admin Extensions: Chats & Messages
    cursor.execute("""
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
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            chat_id TEXT,
            role TEXT,
            content TEXT,
            tokens INTEGER DEFAULT 0,
            flagged INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)
    
    # Law Database Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS law_database (
            id TEXT PRIMARY KEY,
            law_name TEXT,
            category TEXT,
            section_number TEXT,
            chapter TEXT,
            content TEXT,
            summary TEXT,
            keywords TEXT,
            effective_date TEXT,
            repealed_status TEXT DEFAULT 'Active',
            created_at TEXT
        )
    """)
    
    # Knowledge Base Chunks (RAG Preparedness)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id TEXT PRIMARY KEY,
            doc_name TEXT,
            file_type TEXT,
            chunk_content TEXT,
            metadata TEXT,
            created_at TEXT
        )
    """)

    # Dynamic System Prompts Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prompt_templates (
            id TEXT PRIMARY KEY,
            name TEXT UNIQUE,
            system_prompt TEXT,
            version INTEGER DEFAULT 1,
            updated_at TEXT
        )
    """)

    # Subscriptions & Payments
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscription_plans (
            id TEXT PRIMARY KEY,
            name TEXT UNIQUE,
            price_pkr REAL,
            credit_limit INTEGER,
            features TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id TEXT PRIMARY KEY,
            account_id TEXT,
            gateway TEXT,
            trx_id TEXT,
            amount REAL,
            credits_added INTEGER,
            status TEXT DEFAULT 'Pending',
            created_at TEXT
        )
    """)

    # System Logs & Audit Logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id TEXT PRIMARY KEY,
            account_id TEXT,
            action TEXT,
            details TEXT,
            ip_address TEXT,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    conn.commit()
    seed_defaults(conn)

def seed_defaults(conn):
    cursor = conn.cursor()
    # Seed default system prompts if empty
    cursor.execute("SELECT COUNT(*) FROM prompt_templates")
    if cursor.fetchone()[0] == 0:
        now = datetime.now(timezone.utc).isoformat()
        cursor.execute("""
            INSERT INTO prompt_templates (id, name, system_prompt, version, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (str(uuid.uuid4()), "Default Legal Assistant", "You are an expert Pakistani Legal Assistant specializing in Constitution, CrPC, PPC, and PECA.", 1, now))

    # Seed default subscription plans
    cursor.execute("SELECT COUNT(*) FROM subscription_plans")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO subscription_plans VALUES ('p1', 'Free', 0, 5, 'Basic Access, Standard Speed')")
        cursor.execute("INSERT INTO subscription_plans VALUES ('p2', 'Pro Advocate', 1500, 50, 'Priority Gemini 2.5, Document Analysis, Draft Export')")
        cursor.execute("INSERT INTO subscription_plans VALUES ('p3', 'Enterprise Law Firm', 10000, 500, 'Unlimited RAG, Custom Prompts, Priority Support')")
    
    conn.commit()

# --- Credit System Functions ---
def remaining_credits(conn, user_id):
    from config.settings import FREE_QUERY_LIMIT
    cursor = conn.execute("SELECT queries_used FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    used = row[0] if row else 0
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

# FIXED: Added missing functions
def get_all_users(conn):
    """Get all users with their credit usage"""
    return conn.execute("""
        SELECT u.user_id, u.joined_at, u.queries_used, a.email, a.full_name, a.role, a.status
        FROM users u
        LEFT JOIN accounts a ON u.user_id = a.id
        ORDER BY u.joined_at DESC
    """).fetchall()

def add_credits(conn, user_id, amount):
    """Add credits to a user (decrease queries_used)"""
    cursor = conn.execute("SELECT queries_used FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        current_used = row[0]
        new_used = max(0, current_used - amount)  # Don't go below 0
        conn.execute("UPDATE users SET queries_used = ? WHERE user_id = ?", (new_used, user_id))
    else:
        conn.execute("INSERT INTO users (user_id, joined_at, queries_used) VALUES (?, ?, ?)", 
                     (user_id, datetime.now(timezone.utc).isoformat(), 0))
    conn.commit()

def get_user_credits(conn, user_id):
    """Get remaining credits for a user"""
    return remaining_credits(conn, user_id)

# --- Chat Functions ---
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

def delete_chat(conn, chat_id):
    conn.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
    conn.execute("DELETE FROM chats WHERE id = ?", (chat_id,))
    conn.commit()