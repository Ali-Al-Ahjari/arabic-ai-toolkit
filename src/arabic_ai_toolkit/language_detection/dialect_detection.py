from arabic_ai_toolkit.tokenizer.tokenizer import split_words

_DIALECT_KEYWORDS = {
    "Egyptian": {"عايز", "كده", "دلوقتي", "عشان", "ليه", "ايه", "بتاع", "ازيك"},
    "Levantine": {"بدي", "هيك", "شو", "ليش", "كيفك", "منيح", "هلق"},
    "Gulf": {"وايد", "شكو", "وش", "ابغى", "تكفى", "شلونك", "واجد"},
    "Maghrebi": {"بزاف", "ديال", "واش", "شنو", "دابا", "زوين"}
}

def detect_dialect(text: str) -> str:
    """
    Detects Arabic dialect based on specific keywords.
    Returns MSA (Modern Standard Arabic) if no dialect keywords are found.
    """
    words = set(split_words(text))
    
    scores = {dialect: 0 for dialect in _DIALECT_KEYWORDS}
    
    for dialect, keywords in _DIALECT_KEYWORDS.items():
        scores[dialect] = len(words.intersection(keywords))
        
    best_match = max(scores.items(), key=lambda x: x[1])
    
    if best_match[1] > 0:
        return best_match[0]
        
    return "MSA/Unknown"
