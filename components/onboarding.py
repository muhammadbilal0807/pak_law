import uuid
import streamlit as st
from utils.validators import sanitize_user_id

# Extra credits granted once a visitor voluntarily shares a contact.
# Combined with FREE_QUERY_LIMIT (set that to 5 in config/settings.py),
# a verified visitor ends up with 5 + 5 = 10 total.
BONUS_CREDITS = 5


def init_guest_session():
    """Silently gives every visitor a working session -- no signup wall.

    Call this once, near the top of app.py, before conn/client are needed.
    If the URL already has a `uid` (returning visitor, or someone who
    already claimed their bonus), we reuse it. Otherwise we mint a random
    guest id so they can start chatting immediately with their free
    credits, no email or phone number required.
    """
    if st.session_state.get("user_id"):
        return

    existing = st.query_params.get("uid")
    if existing:
        st.session_state.user_id = existing
    else:
        guest_id = f"guest-{uuid.uuid4().hex[:10]}"
        st.session_state.user_id = guest_id
        st.query_params["uid"] = guest_id


def _ensure_bonus_table(conn):
    # Kept separate from the main users table so this feature doesn't
    # require touching database/db.py at all.
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bonus_claims (
            user_id TEXT PRIMARY KEY,
            contact TEXT UNIQUE,
            claimed_at TEXT
        )
    """)
    conn.commit()


def _has_claimed_bonus(conn, user_id):
    row = conn.execute(
        "SELECT 1 FROM bonus_claims WHERE user_id = ?", (user_id,)
    ).fetchone()
    return row is not None


def render_bonus_banner(conn):
    """Small, dismissible banner offering +5 credits for verifying with
    an email or WhatsApp number. Purely optional -- never gates usage,
    never appears again once claimed or dismissed for the session."""
    _ensure_bonus_table(conn)
    user_id = st.session_state.user_id

    if _has_claimed_bonus(conn, user_id):
        return
    if st.session_state.get("bonus_banner_dismissed"):
        return

    st.markdown("""
        <div class="bonus-card animate-fade-in">
            <div class="bonus-card-text">
                🎁 <b>Unlock 5 more free credits</b> — add your email or WhatsApp number (optional).
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        contact = st.text_input(
            "Email or WhatsApp Number",
            key="bonus_contact_input",
            label_visibility="collapsed",
            placeholder="you@company.com or 03xx-xxxxxxx",
        )
    with col2:
        claim = st.button("Claim +5", type="primary", use_container_width=True, key="claim_bonus_btn")
    with col3:
        dismiss = st.button("Not now", use_container_width=True, key="dismiss_bonus_btn")

    if dismiss:
        st.session_state.bonus_banner_dismissed = True
        st.rerun()

    if claim:
        if not contact.strip():
            st.warning("Enter an email or WhatsApp number to claim your bonus credits.")
        else:
            sanitized_contact = sanitize_user_id(contact)
            dup = conn.execute(
                "SELECT 1 FROM bonus_claims WHERE contact = ?", (sanitized_contact,)
            ).fetchone()
            if dup:
                st.error("This contact has already been used to claim a bonus.")
            else:
                from database.db import add_credits
                add_credits(conn, user_id, BONUS_CREDITS)
                conn.execute(
                    "INSERT INTO bonus_claims (user_id, contact, claimed_at) VALUES (?, ?, datetime('now'))",
                    (user_id, sanitized_contact),
                )
                conn.commit()
                st.success(f"🎉 +{BONUS_CREDITS} credits added!")
                st.rerun()