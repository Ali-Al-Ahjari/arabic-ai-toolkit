import re

_ARABIC_CHARS = re.compile(r'[\u0600-\u06FF]')
_ENGLISH_CHARS = re.compile(r'[a-zA-Z]')

def detect_language(text: str) -> str:
    """Detects if text is Arabic, English, Mixed, or Unknown based on character counts."""
    arabic_count = len(_ARABIC_CHARS.findall(text))
    english_count = len(_ENGLISH_CHARS.findall(text))
    
    if arabic_count == 0 and english_count == 0:
        return "Unknown"
    elif arabic_count > 0 and english_count == 0:
        return "Arabic"
    elif english_count > 0 and arabic_count == 0:
        return "English"
    else:
        return "Mixed"
