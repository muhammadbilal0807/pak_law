import bcrypt
import uuid
from datetime import datetime, timezone
import streamlit as st

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register_user(conn, email, password, full_name, phone=""):
    cursor = conn.execute("SELECT id FROM accounts WHERE email = ?", (email,))
    if cursor.fetchone():
        return False, "Email already exists."
    
    account_id = str(uuid.uuid4())
    hashed_pw = hash_password(password)
    now = datetime.now(timezone.utc).isoformat()
    role = "User"
    
    conn.execute("""
        INSERT INTO accounts (id, email, password_hash, full_name, phone, role, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (account_id, email, hashed_pw, full_name, phone, role, now))
    
    # Initialize settings and link to legacy credits
    conn.execute("INSERT INTO settings (account_id, theme, language, notifications) VALUES (?, 'Light', 'English', 1)", (account_id,))
    conn.execute("INSERT INTO users (user_id, joined_at, queries_used) VALUES (?, ?, 0)", (account_id, now))
    conn.commit()
    
    return True, account_id

def authenticate_user(conn, email, password):
    cursor = conn.execute("SELECT id, password_hash, full_name, role FROM accounts WHERE email = ?", (email,))
    row = cursor.fetchone()
    if row and verify_password(password, row[1]):
        return True, {"id": row[0], "full_name": row[2], "role": row[3], "email": email}
    return False, "Invalid email or password."

def logout():
    for key in ["user", "user_id", "current_chat_id", "messages_by_mode"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()