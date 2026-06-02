from collections import Counter
from arabic_ai_toolkit.tokenizer.tokenizer import split_words
from arabic_ai_toolkit.stopwords.stopwords import remove_stopwords

def extract_keywords(text: str, top_n: int = 5) -> list[tuple[str, int]]:
    """
    Extracts top N keywords based on term frequency.
    Basic implementation.
    """
    words = split_words(text)
    words = remove_stopwords(words)
    counter = Counter(words)
    return counter.most_common(top_n)
