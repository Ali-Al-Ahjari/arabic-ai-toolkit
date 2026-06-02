import re

# Arabic diacritics
_DIACRITICS = re.compile(r'[\u064B-\u0652]')
# Tatweel (Kashida)
_TATWEEL = re.compile(r'\u0640')
# URLs
_URLS = re.compile(r'https?://\S+|www\.\S+')
# Punctuation (Arabic and English standard)
_PUNCTUATION = re.compile(r'[!\"#\$%&\'\(\)\*\+,\-\./:;<=>\?@\[\\\]\^_`\{\|\}~،؛؟«»]')
# Emojis (Simple unicode range approach, can be expanded)
_EMOJIS = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)

def remove_diacritics(text: str) -> str:
    """Removes Arabic diacritics (Tashkeel) from text."""
    return _DIACRITICS.sub('', text)

def remove_tatweel(text: str) -> str:
    """Removes Tatweel (Kashida) from text."""
    return _TATWEEL.sub('', text)

def remove_urls(text: str) -> str:
    """Removes URLs from text."""
    return _URLS.sub('', text)

def remove_punctuation(text: str) -> str:
    """Removes punctuation from text."""
    return _PUNCTUATION.sub('', text)

def remove_emojis(text: str) -> str:
    """Removes emojis from text."""
    return _EMOJIS.sub('', text)

def normalize_spaces(text: str) -> str:
    """Removes extra spaces from text."""
    return re.sub(r'\s+', ' ', text).strip()

def clean(text: str, 
          diacritics: bool = True, 
          tatweel: bool = True, 
          urls: bool = True, 
          punctuation: bool = False, 
          emojis: bool = False,
          spaces: bool = True) -> str:
    """
    Cleans the Arabic text based on the provided flags.
    By default, removes diacritics, tatweel, urls, and normalizes spaces.
    """
    if urls:
        text = remove_urls(text)
    if emojis:
        text = remove_emojis(text)
    if punctuation:
        text = remove_punctuation(text)
    if diacritics:
        text = remove_diacritics(text)
    if tatweel:
        text = remove_tatweel(text)
    if spaces:
        text = normalize_spaces(text)
    return text
