iimport os

PAGE_TITLE = "Pak Law AI — Enterprise Platform"
FREE_QUERY_LIMIT = 5
COOLDOWN_SECONDS = 3.0
MAX_HISTORY_MESSAGES = 10

MODES = ["Legal Q&A", "Drafting", "Analysis"]

# Pricing & Upgrade Configuration
UPGRADE_CREDITS = 50
UPGRADE_PRICE_PKR = 1500
JAZZCASH_NUMBER = "0303-7154605"
EASYPAISA_NUMBER = "0339-4111973"
WHATSAPP_NUMBER = "+923037154605"

# RBAC Roles
ROLE_USER = "User"
ROLE_MODERATOR = "Moderator"
ROLE_ADMIN = "Admin"
ROLE_SUPER_ADMIN = "Super Admin"
ADMIN_ROLES = [ROLE_ADMIN, ROLE_SUPER_ADMIN]

# Gemini AI Hyperparameters & Defaults
DEFAULT_AI_CONFIG = {
    "model_name": "gemini-3.5-flash",
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_tokens": 2048,
    "context_window": 8192,
    "streaming": True
}

# Primary Model Export (Resolves the ImportError)
PRIMARY_MODEL = DEFAULT_AI_CONFIG["model_name"]

MODE_MAX_TOKENS = {
    "Legal Q&A": 1500,
    "Drafting": 3000,
    "Analysis": 2500
}