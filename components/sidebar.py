import streamlit as st
from config.settings import (
    FREE_QUERY_LIMIT, MODES, UPGRADE_CREDITS, UPGRADE_PRICE_PKR, 
    JAZZCASH_NUMBER, EASYPAISA_NUMBER, WHATSAPP_NUMBER
)
from components.admin import render_admin_panel

def render_sidebar(conn, credits_left):
    """Renders the full sidebar and returns the selected app mode."""
    with st.sidebar:
        st.title("⚖️ Pak Law AI")

        # Progress bar safely capped
        progress_val = min(max(credits_left, 0), FREE_QUERY_LIMIT) / FREE_QUERY_LIMIT if credits_left <= FREE_QUERY_LIMIT else 1.0
        st.progress(progress_val)
        st.caption(f"Credits left: {max(credits_left, 0)}")

        if credits_left <= 0:
            st.error(f"Free limit reached. Buy {UPGRADE_CREDITS} more credits for Rs {UPGRADE_PRICE_PKR}.")

        st.divider()

        if st.button("➕ New Chat"):
            st.session_state.messages_by_mode = {m: [] for m in MODES}
            st.rerun()

        st.markdown("### 🛠️ AI Tools")
        app_mode = st.radio("Select Mode:", MODES, key="app_mode_radio")

        st.divider()
        with st.expander("💳 Buy More Credits"):
            st.write(
                f"Send **Rs. {UPGRADE_PRICE_PKR}** for {UPGRADE_CREDITS} credits to:\n\n"
                f"- JazzCash: `{JAZZCASH_NUMBER}`\n"
                f"- Easypaisa: `{EASYPAISA_NUMBER}`\n\n"
                f"(Stripe isn't a practical option here - it doesn't support Pakistan-registered "
                f"businesses directly.) Send the payment screenshot on WhatsApp and we'll add your credits."
            )
            user_id = st.session_state.get("user_id", "")
            st.link_button(
                "📲 Send screenshot on WhatsApp",
                f"https://wa.me/{WHATSAPP_NUMBER}?text=Hi%2C%20I%20paid%20for%20Pak%20Law%20AI%20credits.%20My%20ID%3A%20{user_id}"
            )

        st.divider()
        st.markdown("### 💬 Recent Queries")
        if not st.session_state.get("history_titles"):
            st.caption("No queries yet.")
        else:
            for title in reversed(st.session_state.history_titles[-5:]):
                st.markdown(f"• **{title}**")

        render_admin_panel(conn)
        
    return app_mode