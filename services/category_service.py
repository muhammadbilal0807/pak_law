CATEGORY_KEYWORDS = {
    "🚔 Criminal": ["fir", "arrest", "police", "murder", "theft", "assault", "bail", "ppc", "crpc", "crime"],
    "💻 Cybercrime": ["cyber", "hack", "peca", "online harassment", "blackmail", "leaked", "social media", "whatsapp", "facebook"],
    "👨‍👩‍👧 Family": ["divorce", "khula", "custody", "nikah", "marriage", "inheritance", "dowry", "maintenance"],
    "🏠 Property": ["property", "tenant", "eviction", "land", "rent", "lease", "possession"],
    "🏛️ Constitutional": ["fundamental right", "constitution", "article "],
}

def detect_category(text: str) -> str:
    t = text.lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in t for kw in keywords):
            return cat
    return "⚖️ General Legal"