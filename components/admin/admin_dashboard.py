import streamlit as st
import plotly.express as px
import pandas as pd

from services.admin_service import get_dashboard_metrics

def render_admin_dashboard(conn):
    st.markdown('<div class="admin-header">Enterprise Executive Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="admin-subheader">Real-time usage metrics, financial totals, and API performance.</div>', unsafe_allow_html=True)
    
    metrics = get_dashboard_metrics(conn)

    # Metric Row 1
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="admin-card">
                <div class="admin-card-title">Total Users</div>
                <div class="admin-card-value">{metrics['total_users']}</div>
                <div class="admin-card-delta">🟢 {metrics['active_users']} Active</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="admin-card">
                <div class="admin-card-title">Total Queries Executed</div>
                <div class="admin-card-value">{metrics['total_queries']}</div>
                <div class="admin-card-delta">⚡ Across {metrics['total_chats']} Chats</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="admin-card">
                <div class="admin-card-title">Total Revenue</div>
                <div class="admin-card-value">PKR {metrics['total_revenue']:,.0f}</div>
                <div class="admin-card-delta">💳 {metrics['pending_payments']} Pending Approvals</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class="admin-card">
                <div class="admin-card-title">Token Volume</div>
                <div class="admin-card-value">{metrics['total_tokens']:,}</div>
                <div class="admin-card-delta">🤖 Gemini 2.5 Flash</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Plotly Charts
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 📈 Usage & Activity Trends")
        # Generate dummy trend chart from actual page views DB
        pv_df = pd.read_sql_query("SELECT timestamp FROM page_views", conn)
        if not pv_df.empty:
            pv_df['date'] = pd.to_datetime(pv_df['timestamp']).dt.date
            trend_df = pv_df.groupby('date').size().reset_index(name='Sessions')
            fig = px.area(trend_df, x='date', y='Sessions', title="Daily Application Volume", template="plotly_dark")
            fig.update_traces(line_color="#0284C7")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No session activity logs recorded yet.")

    with col2:
        st.markdown("### 📚 Law DB Composition")
        laws_df = pd.read_sql_query("SELECT category, COUNT(*) as count FROM law_database GROUP BY category", conn)
        if not laws_df.empty:
            fig_pie = px.pie(laws_df, names='category', values='count', hole=0.4, template="plotly_dark")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.caption("No laws added to database yet.")