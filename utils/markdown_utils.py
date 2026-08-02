import re

def markdown_to_plain(md_text: str) -> str:
    """Strip Markdown syntax (###, **bold**, etc.) so downloaded .txt files
    read as clean plain text instead of showing raw asterisks/hashes."""
    text = md_text
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)   # ### headings
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)                 # **bold**
    text = re.sub(r'__(.*?)__', r'\1', text)                     # __bold__
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'\1', text)  # *italic*
    text = re.sub(r'`([^`]*)`', r'\1', text)                     # `code`
    return text.strip()