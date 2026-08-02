import streamlit as st

def load_admin_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

        /* Admin Layout Theme */
        .stApp {
            background-color: #0F172A !important;
            color: #F8FAFC !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #1E293B !important;
            border-right: 1px solid #334155 !important;
        }

        /* Metric Cards */
        .admin-card {
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        }
        .admin-card-title {
            color: #94A3B8;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .admin-card-value {
            color: #F8FAFC;
            font-size: 2.2rem;
            font-weight: 700;
            margin-top: 8px;
        }
        .admin-card-delta {
            color: #10B981;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 4px;
        }

        /* Admin Table Containers */
        .stDataFrame {
            border: 1px solid #334155 !important;
            border-radius: 10px !important;
        }

        /* Badges */
        .badge-active { background: #064E3B; color: #34D399; padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; }
        .badge-suspended { background: #7F1D1D; color: #FCA5A5; padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; }
        .badge-admin { background: #312E81; color: #A5B4FC; padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; }
        
        /* Headers */
        .admin-header {
            font-size: 1.75rem;
            font-weight: 700;
            color: #F8FAFC;
            margin-bottom: 0.5rem;
        }
        .admin-subheader {
            font-size: 0.95rem;
            color: #94A3B8;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)