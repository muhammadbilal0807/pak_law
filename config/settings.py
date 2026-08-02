import os

PAGE_TITLE = "Pak Law AI — Enterprise Platform"
FREE_QUERY_LIMIT = 5
COOLDOWN_SECONDS = 3.0
MAX_HISTORY_MESSAGES = 10

MODES = ["Legal Q&A", "Drafting", "Analysis"]

# Pricing & Upgrade Configuration
UPGRADE_CREDITS = 50
UPGRADE_PRICE_PKR = 1500
JAZZCASH_NUMBER = "0300-1234567"
EASYPAISA_NUMBER = "0345-7654321"
WHATSAPP_NUMBER = "923001234567"

# RBAC Roles
ROLE_USER = "User"
ROLE_MODERATOR = "Moderator"
ROLE_ADMIN = "Admin"
ROLE_SUPER_ADMIN = "Super Admin"
ADMIN_ROLES = [ROLE_ADMIN, ROLE_SUPER_ADMIN]

# Gemini AI Hyperparameters & Defaults
DEFAULT_AI_CONFIG = {
    "model_name": "gemini-2.5-flash",
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_tokens": 2048,
    "context_window": 8192,
    "streaming": True
}

MODE_MAX_TOKENS = {
    "Legal Q&A": 1500,
    "Drafting": 3000,
    "Analysis": 2500
}