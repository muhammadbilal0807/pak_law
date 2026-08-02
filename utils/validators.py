def sanitize_user_id(raw: str) -> str:
    """Sanitizes user ID input."""
    raw = raw.strip().lower()
    if "@" in raw:
        return raw
    return "".join(ch for ch in raw if ch.isdigit())