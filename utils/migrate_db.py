# utils/migrate_db.py
import sqlite3
from database.db import DB_FILE

def migrate_database():
    """Run database migrations for schema updates."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check if settings table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='settings'")
    if not cursor.fetchone():
        cursor.execute("""
            CREATE TABLE settings (
                account_id TEXT PRIMARY KEY,
                theme TEXT DEFAULT 'Light',
                language TEXT DEFAULT 'English',
                notifications INTEGER DEFAULT 1
            )
        """)
    
    # Check for any other missing tables
    required_tables = ['chats', 'messages', 'law_database', 'knowledge_base', 
                       'prompt_templates', 'subscription_plans', 'payments', 
                       'audit_logs', 'system_settings']
    
    for table in required_tables:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        if not cursor.fetchone():
            print(f"Table {table} is missing. Please run the app to create it.")
    
    conn.commit()
    conn.close()
    print("Migration completed successfully.")

if __name__ == "__main__":
    migrate_database()