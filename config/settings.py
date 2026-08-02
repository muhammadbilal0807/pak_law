# =====================================================================
# 0. CONFIG - edit these before you launch
# =====================================================================
PAGE_TITLE = "Pak Law AI - Legal Assistant"

FREE_QUERY_LIMIT = 5
MAX_HISTORY_MESSAGES = 4     # last 2 exchanges - keeps token cost low
COOLDOWN_SECONDS = 3         # min seconds between sends per user (anti-spam)

PRIMARY_MODEL = "gemini-3.6-flash"
FALLBACK_MODEL = "gemini-3.5-flash-lite"

MODES = ["Legal Q&A", "Draft FIR", "Draft Legal Notice"]
MODE_MAX_TOKENS = {"Legal Q&A": 1024, "Draft FIR": 1536, "Draft Legal Notice": 1536}

DB_PATH = "usage.db"

# --- Fill these in with your real details before going live ---
JAZZCASH_NAME = "MUHAMMAD BILAL"
JAZZCASH_NUMBER = "0303-7154605"
EASYPAISA_NAME = "NAEEM AHMAD"
EASYPAISA_NUMBER = "0339-4111973"
WHATSAPP_NUMBER = "+923037154605"      # country code + number, no "+", no spaces
UPGRADE_PRICE_PKR = 100
UPGRADE_CREDITS = 30