import streamlit as st
from streamlit_option_menu import option_menu
from config.settings import (
    FREE_QUERY_LIMIT, MODES, UPGRADE_CREDITS, UPGRADE_PRICE_PKR, 
    JAZZCASH_NUMBER, EASYPAISA_NUMBER, WHATSAPP_NUMBER
)
from components.admin import render_admin_panel

def render_sidebar(conn, credits_left):
    """Renders the premium SaaS navigation panel."""
    with st.sidebar:
        # App Logo & Name
        st.markdown("""
            <div class="sidebar-logo animate-fade-in">
                ⚖️ Pak Law AI
            </div>
        """, unsafe_allow_html=True)

        # New Chat Button
        if st.button("➕ New Conversation", type="primary", use_container_width=True):
            st.session_state.messages_by_mode = {m: [] for m in MODES}
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)

        # Custom Credit Card UI
        capped_credits = max(credits_left, 0)
        progress_val = min(capped_credits, FREE_QUERY_LIMIT) / FREE_QUERY_LIMIT if capped_credits <= FREE_QUERY_LIMIT else 1.0
        
        st.markdown(f"""
            <div class="credit-card">
                <div class="credit-title">Available Credits</div>
                <div class="credit-value">{capped_credits}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Wrapping progress bar in layout columns to match margins of the card
        c1, c2, c3 = st.columns([0.05, 0.9, 0.05])
        with c2:
            st.progress(progress_val)
        
        if credits_left <= 0:
            st.error("Free limit reached. Upgrade required.")

        st.markdown("<br>", unsafe_allow_html=True)

        # Premium Navigation Menu using option_menu
        st.markdown("<span style='color:#94A3B8; font-size:0.75rem; font-weight:600; text-transform:uppercase; padding-left:15px; letter-spacing:0.5px;'>AI Tools</span>", unsafe_allow_html=True)
        
        app_mode = option_menu(
            menu_title=None,
            options=MODES,
            icons=['chat-left-text', 'file-earmark-text', 'envelope-paper'],
            default_index=MODES.index(st.session_state.get("last_mode", MODES[0])) if "last_mode" in st.session_state else 0,
            styles={
                "container": {"padding": "0 10px", "background-color": "transparent"},
                "icon": {"color": "#64748B", "font-size": "15px"}, 
                "nav-link": {"font-size": "14px", "text-align": "left", "margin":"4px 0", "color": "#334155", "border-radius": "8px"},
                "nav-link-selected": {"background-color": "#F1F5F9", "color": "#0F766E", "font-weight": "600", "icon-color": "#0F766E"},
            }
        )
        st.session_state.last_mode = app_mode

        st.markdown("<br>", unsafe_allow_html=True)

        # Upgrade Section
        with st.expander("💳 Upgrade Plan"):
            st.markdown(f"""
                <div style="font-size:0.9rem; color:#475569; margin-bottom:12px;">
                    Get <b>{UPGRADE_CREDITS} queries</b> for just <b>Rs. {UPGRADE_PRICE_PKR}</b>.
                </div>
                <div style="background:#F8FAFC; padding:12px; border:1px solid #E2E8F0; border-radius:8px; font-family:monospace; font-size:0.85rem; margin-bottom:12px; color:#334155;">
                    JazzCash: {JAZZCASH_NUMBER}<br>
                    Easypaisa: {EASYPAISA_NUMBER}
                </div>
            """, unsafe_allow_html=True)
            user_id = st.session_state.get("user_id", "")
            st.link_button(
                "Verify via WhatsApp",
                f"https://wa.me/{WHATSAPP_NUMBER}?text=Hi%2C%20I%20paid%20for%20Pak%20Law%20AI%20credits.%20My%20ID%3A%20{user_id}",
                use_container_width=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Recent Queries
        st.markdown("<span style='color:#94A3B8; font-size:0.75rem; font-weight:600; text-transform:uppercase; padding-left:15px; letter-spacing:0.5px;'>Recent Activity</span>", unsafe_allow_html=True)
        if not st.session_state.get("history_titles"):
            st.markdown("<div style='padding-left:15px; color:#94A3B8; font-size:0.85rem; margin-top:5px;'>No recent queries.</div>", unsafe_allow_html=True)
        else:
            for title in reversed(st.session_state.history_titles[-5:]):
                clean_title = title.split("] ")[-1]
                st.markdown(f"""
                    <div style="padding: 8px 15px; font-size: 0.85rem; color: #475569; cursor: pointer; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                        <span style="opacity:0.4; margin-right:8px;">💬</span> {clean_title}
                    </div>
                """, unsafe_allow_html=True)

        render_admin_panel(conn)
        
    return app_mode