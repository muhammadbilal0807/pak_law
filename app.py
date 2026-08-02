import streamlit as st
from config.settings import PAGE_TITLE, MODES
from database.db import init_db
import sqlite3
from services.gemini_service import get_ai_response

# Initialize the database when the app loads
init_db()

st.set_page_config(page_title=PAGE_TITLE, layout="centered")

st.title("⚖️ Pak Law AI")
st.write("Your intelligent legal assistant workspace.")

# Sidebar mode selection
selected_mode = st.sidebar.selectbox("Choose Mode", MODES)

# Main input area
user_query = st.text_area("Enter your legal question or query here:")

if st.button("Generate Response"):
    if user_query.strip() == "":
        st.warning("Please enter a question before submitting.")
    else:
        with st.spinner("Analyzing with Gemini..."):
            try:
                # Fetch response from Gemini service
                response_text = get_ai_response(user_query)
                
                # Display the response
                st.subheader("Response")
                st.write(response_text)

                # Save the interaction to the SQLite database
                conn = sqlite3.connect("database/pak_law.db")
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO queries (timestamp, query, response, mode) VALUES (datetime('now'), ?, ?, ?)",
                    (user_query, response_text, selected_mode)
                )
                conn.commit()
                conn.close()
            except Exception as e:
                st.error(f"An error occurred: {e}")