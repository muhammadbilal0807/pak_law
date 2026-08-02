import sqlite3

DB_NAME = "database/pak_law.db"

def init_db():
    """Initializes the SQLite database and creates the queries table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            query TEXT,
            response TEXT,
            mode TEXT
        )
    ''')
    conn.commit()
    conn.close()