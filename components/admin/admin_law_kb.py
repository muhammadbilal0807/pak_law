import streamlit as st
import pandas as pd
from services.law_kb_service import add_law_entry, search_laws, ingest_knowledge_document
from services.admin_service import log_audit_action

def render_admin_law_kb(conn, is_kb_mode=False):
    if not is_kb_mode:
        st.markdown('<div class="admin-header">Pakistani Statutes Database</div>', unsafe_allow_html=True)
        st.markdown('<div class="admin-subheader">Manage legal codes, sections, summaries, and keywords referenced by Gemini.</div>', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["📜 Law Explorer", "➕ Add New Law Entry"])
        
        with tab1:
            q = st.text_input("Filter Law Entries")
            df_laws = search_laws(conn, q)
            st.dataframe(df_laws, use_container_width=True, hide_index=True)

        with tab2:
            with st.form("add_law_form"):
                col_l1, col_l2 = st.columns(2)
                with col_l1:
                    law_name = st.text_input("Law Title (e.g. Pakistan Penal Code)")
                    category = st.selectbox("Category", ["Criminal", "Civil", "Constitutional", "Corporate", "Cyber Law", "Family Law"])
                    section = st.text_input("Section Number (e.g. Section 302)")
                with col_l2:
                    chapter = st.text_input("Chapter (e.g. Chapter XVI)")
                    keywords = st.text_input("Keywords (comma separated)")
                
                content = st.text_area("Full Legal Text Content", height=150)
                summary = st.text_area("Plain English Summary", height=80)
                
                if st.form_submit_button("Save Law Entry", type="primary"):
                    if law_name and content:
                        add_law_entry(conn, law_name, category, section, chapter, content, summary, keywords)
                        log_audit_action(conn, st.session_state.user["id"], "ADD_LAW", f"Added {law_name} - {section}")
                        st.success(f"Added {law_name} {section} successfully.")
                        st.rerun()
                    else:
                        st.error("Law Title and Legal Text are required.")
    else:
        st.markdown('<div class="admin-header">Knowledge Base & Chunk Ingestion</div>', unsafe_allow_html=True)
        st.markdown('<div class="admin-subheader">Upload legal reference documents (PDF/TXT) to prepare index chunks for RAG context.</div>', unsafe_allow_html=True)
        
        uploaded_doc = st.file_uploader("Upload Legal Document (PDF or TXT)", type=["pdf", "txt"])
        chunk_size = st.slider("Chunk Character Size", min_value=300, max_value=2000, value=1000, step=100)
        
        if uploaded_doc and st.button("Process & Chunk Document", type="primary"):
            text = ""
            if uploaded_doc.name.endswith(".pdf"):
                import PyPDF2
                reader = PyPDF2.PdfReader(uploaded_doc)
                for page in reader.pages:
                    text += page.extract_text() or ""
            else:
                text = uploaded_doc.read().decode("utf-8")
                
            num_chunks = ingest_knowledge_document(conn, uploaded_doc.name, uploaded_doc.type, text, chunk_size)
            log_audit_action(conn, st.session_state.user["id"], "INGEST_KB", f"Ingested {uploaded_doc.name} into {num_chunks} chunks.")
            st.success(f"Successfully processed into {num_chunks} searchable chunks.")
        
        st.divider()
        st.markdown("### 🔍 Existing Knowledge Base Chunks")
        df_kb = pd.read_sql_query("SELECT id, doc_name, file_type, created_at FROM knowledge_base ORDER BY created_at DESC", conn)
        st.dataframe(df_kb, use_container_width=True, hide_index=True)