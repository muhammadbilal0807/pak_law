import streamlit as st
import plotly.express as px
import pandas as pd

def render_admin_analytics(conn):
    st.markdown('<div class="admin-header">System Analytics & Growth Metrics</div>', unsafe_allow_html=True)
    st.markdown('<div class="admin-subheader">Detailed statistics regarding user retention, tokens consumed, and workspace activity.</div>', unsafe_allow_html=True)

    df_msgs = pd.read_sql_query("SELECT role, tokens, created_at FROM messages", conn)
    
    if not df_msgs.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📊 Token Distribution by Role")
            fig_tokens = px.histogram(df_msgs, x="tokens", color="role", barmode="overlay", template="plotly_dark")
            st.plotly_chart(fig_tokens, use_container_width=True)

        with col2:
            st.markdown("### 💬 Assistant vs User Volume")
            role_counts = df_msgs["role"].value_counts().reset_index()
            role_counts.columns = ["Role", "Messages"]
            fig_roles = px.bar(role_counts, x="Role", y="Messages", color="Role", template="plotly_dark")
            st.plotly_chart(fig_roles, use_container_width=True)
    else:
        st.info("Insufficient message data to construct analytics visualizations.")