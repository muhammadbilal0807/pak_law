import uuid
from datetime import datetime, timezone
import pandas as pd

def add_law_entry(conn, law_name, category, section, chapter, content, summary, keywords):
    law_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    conn.execute("""
        INSERT INTO law_database (id, law_name, category, section_number, chapter, content, summary, keywords, effective_date, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (law_id, law_name, category, section, chapter, content, summary, keywords, now[:10], now))
    conn.commit()
    return law_id

def search_laws(conn, query_str=""):
    if not query_str:
        return pd.read_sql_query("SELECT id, law_name, category, section_number, chapter, effective_date FROM law_database ORDER BY created_at DESC", conn)
    
    pattern = f"%{query_str}%"
    sql = """
        SELECT id, law_name, category, section_number, chapter, effective_date
        FROM law_database
        WHERE law_name LIKE ? OR category LIKE ? OR content LIKE ? OR keywords LIKE ?
    """
    return pd.read_sql_query(sql, conn, params=(pattern, pattern, pattern, pattern))

def ingest_knowledge_document(conn, doc_name, file_type, text_content, chunk_size=1000):
    """Splits large text files into RAG-ready chunks and stores metadata."""
    chunks = [text_content[i:i+chunk_size] for i in range(0, len(text_content), chunk_size)]
    now = datetime.now(timezone.utc).isoformat()
    
    for i, chunk in enumerate(chunks):
        chunk_id = str(uuid.uuid4())
        metadata = f'{{"doc": "{doc_name}", "chunk_index": {i}}}'
        conn.execute("""
            INSERT INTO knowledge_base (id, doc_name, file_type, chunk_content, metadata, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (chunk_id, doc_name, file_type, chunk, metadata, now))
    conn.commit()
    return len(chunks)