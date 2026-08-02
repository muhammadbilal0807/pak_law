# css/admin_styles.py
import streamlit as st

def load_admin_css():
    """Load custom CSS for the admin workspace"""
    st.markdown("""
    <style>
        /* Admin Header */
        .admin-header {
            font-size: 1.8rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 0.5rem;
        }
        
        .admin-subheader {
            font-size: 1rem;
            color: #64748B;
            margin-bottom: 2rem;
        }
        
        /* Admin Cards */
        .admin-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #E2E8F0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: all 0.2s;
        }
        
        .admin-card:hover {
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        
        .admin-card-title {
            font-size: 0.85rem;
            font-weight: 500;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .admin-card-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #0F172A;
            margin: 0.5rem 0;
        }
        
        .admin-card-delta {
            font-size: 0.85rem;
            color: #0284C7;
        }
        
        /* Admin Sidebar */
        .admin-sidebar-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #38BDF8;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* Admin Tables */
        .admin-table-container {
            background: white;
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid #E2E8F0;
            margin: 1rem 0;
        }
        
        /* Admin Buttons */
        .admin-button-primary {
            background: #0284C7;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .admin-button-primary:hover {
            background: #0369A1;
            transform: translateY(-2px);
        }
    </style>
    """, unsafe_allow_html=True)