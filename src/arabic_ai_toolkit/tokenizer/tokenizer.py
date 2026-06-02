import re

# Split by whitespace for basic word tokenization
# We also need to separate punctuation from words.
_PUNCTUATION_REGEX = re.compile(r'([!\"#\$%&\'\(\)\*\+,\-\./:;<=>\?@\[\\\]\^_`\{\|\}~،؛؟«»])')

def split_words(text: str) -> list[str]:
    """
    Splits text into words.
    Basic implementation: separates punctuation and then splits by whitespace.
    """
    # Pad punctuation with spaces so they become separate tokens
    padded = _PUNCTUATION_REGEX.sub(r' \1 ', text)
    # Split by whitespace
    return [word for word in padded.split() if word.strip()]

def split_sentences(text: str) -> list[str]:
    """
    Splits text into sentences based on common Arabic and English sentence delimiters.
    Delimiters: '.', '!', '?', '؟'
    """
    # Split using a regex that looks behind for sentence terminators
    sentences = re.split(r'(?<=[.!?؟])\s+', text)
    return [s.strip() for s in sentences if s.strip()]
