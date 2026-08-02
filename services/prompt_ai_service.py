import pandas as pd
from datetime import datetime, timezone

def get_all_prompts(conn):
    return pd.read_sql_query("SELECT id, name, version, updated_at FROM prompt_templates", conn)

def update_prompt_template(conn, name, new_system_prompt):
    now = datetime.now(timezone.utc).isoformat()
    cursor = conn.execute("SELECT version FROM prompt_templates WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row:
        new_version = row[0] + 1
        conn.execute("""
            UPDATE prompt_templates
            SET system_prompt = ?, version = ?, updated_at = ?
            WHERE name = ?
        """, (new_system_prompt, new_version, now, name))
    else:
        import uuid
        conn.execute("""
            INSERT INTO prompt_templates (id, name, system_prompt, version, updated_at)
            VALUES (?, ?, ?, 1, ?)
        """, (str(uuid.uuid4()), name, new_system_prompt, now))
    conn.commit()

def save_system_setting(conn, key, value):
    conn.execute("INSERT OR REPLACE INTO system_settings (key, value) VALUES (?, ?)", (key, str(value)))
    conn.commit()

def get_system_setting(conn, key, default=None):
    row = conn.execute("SELECT value FROM system_settings WHERE key = ?", (key,)).fetchone()
    return row[0] if row else default