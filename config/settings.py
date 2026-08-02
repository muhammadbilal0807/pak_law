# config/settings.py
import os

# App Configuration
PAGE_TITLE = "Pak Law AI - Legal Assistant"
MODES = ["Legal Q&A", "Drafting", "Analysis"]
ADMIN_ROLES = ["Admin", "Super Admin"]

# Credit System
FREE_QUERY_LIMIT = 10  # Free tier queries
UPGRADE_CREDITS = 50   # Default credits for upgrades

# AI Model Configuration
PRIMARY_MODEL = "gemini-2.5-flash"
FALLBACK_MODEL = "gemini-2.5-pro"

DEFAULT_AI_CONFIG = {
    "model_name": "gemini-2.5-flash",
    "temperature": 0.7,
    "max_tokens": 1500,
    "thinking_level": "LOW"
}

# Security
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")  # Change in production!

# Database
DB_FILE = "pak_law_ai.db"