import streamlit as st
from streamlit_option_menu import option_menu
from config.settings import (
    FREE_QUERY_LIMIT, MODES, UPGRADE_CREDITS, UPGRADE_PRICE_PKR, 
    JAZZCASH_NUMBER, EASYPAISA_NUMBER, WHATSAPP_NUMBER
)
from components.admin import render_admin_panel

def render_sidebar(conn, credits_left):
    """Renders the professional enterprise SaaS sidebar."""
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-logo animate-fade-in">
                ⚖️ Pak Law AI
            </div>
        """, unsafe_allow_html=True)

        if st.button("➕ New Conversation", type="primary", use_container_width=True):
            st.session_state.messages_by_mode = {m: [] for m in MODES}
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)

        capped_credits = max(credits_left, 0)
        # Denominator scales up automatically for anyone who claimed the
        # +5 bonus banner (5 -> 10 total), instead of capping visually at
        # the base FREE_QUERY_LIMIT.
        progress_max = max(FREE_QUERY_LIMIT, capped_credits)
        progress_val = capped_credits / progress_max if progress_max else 0
        
        st.markdown(f"""
            <div class="credit-card">
                <div class="credit-title">Available Credits</div>
                <div class="credit-value">{capped_credits}</div>
            </div>
        """, unsafe_allow_html=True)
        st.progress(progress_val)
        
        if credits_left <= 0:
            st.error("Free limit reached. Upgrade required.")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<span style='color:#64748B; font-size:0.75rem; font-weight:600; text-transform:uppercase; padding-left:10px; letter-spacing:0.05em;'>AI Tools</span>", unsafe_allow_html=True)
        
        app_mode = option_menu(
            menu_title=None,
            options=MODES,
            icons=['chat-left-text', 'file-earmark-text', 'envelope-paper'],
            default_index=MODES.index(st.session_state.get("last_mode", MODES[0])) if "last_mode" in st.session_state else 0,
            styles={
                "container": {"padding": "0!important", "background-color": "#FFFFFF"},
                "icon": {"color": "#64748B", "font-size": "15px"}, 
                "nav-link": {"font-size": "13.5px", "text-align": "left", "margin":"4px 0", "color": "#1E293B", "border-radius": "6px", "background-color": "#FFFFFF"},
                "nav-link-selected": {"background-color": "#F1F5F9", "color": "#0F172A", "font-weight": "600", "icon-color": "#0F172A"},
            }
        )
        st.session_state.last_mode = app_mode

        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("💳 Upgrade Plan"):
            st.markdown(f"""
                <div style="font-size:0.85rem; color:#475569; margin-bottom:10px;">
                    Get <b>{UPGRADE_CREDITS} queries</b> for just <b>Rs. {UPGRADE_PRICE_PKR}</b>.
                </div>
                <div style="background:#F8FAFC; padding:10px; border:1px solid #E2E8F0; border-radius:6px; font-family:monospace; font-size:0.8rem; margin-bottom:10px; color:#334155;">
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

        st.markdown("<span style='color:#64748B; font-size:0.75rem; font-weight:600; text-transform:uppercase; padding-left:10px; letter-spacing:0.05em;'>Recent Activity</span>", unsafe_allow_html=True)
        if not st.session_state.get("history_titles"):
            st.markdown("<div style='padding-left:10px; color:#94A3B8; font-size:0.85rem; margin-top:4px;'>No recent queries.</div>", unsafe_allow_html=True)
        else:
            for title in reversed(st.session_state.history_titles[-5:]):
                clean_title = title.split("] ")[-1]
                st.markdown(f"""
                    <div style="padding: 6px 10px; font-size: 0.85rem; color: #475569; cursor: pointer; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                        <span style="opacity:0.5; margin-right:6px;">💬</span> {clean_title}
                    </div>
                """, unsafe_allow_html=True)

        render_admin_panel(conn)
        
    return app_mode