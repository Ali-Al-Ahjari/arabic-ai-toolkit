from arabic_ai_toolkit.tokenizer.tokenizer import split_words
from arabic_ai_toolkit.normalizer.normalizer import normalize

# Very basic lexicons
_POSITIVE = {"ممتاز", "رائع", "جيد", "جميل", "عظيم", "مذهل", "احب", "سعيد", "رائعة", "ابداع", "ممتع"}
_NEGATIVE = {"سيء", "حزين", "قبيح", "رديء", "اكره", "مزعج", "فاشل", "ممل", "غبي", "ضعيف"}

def analyze_sentiment(text: str) -> dict:
    """
    Returns sentiment scores based on word counts.
    """
    words = split_words(normalize(text))
    pos_count = sum(1 for w in words if w in _POSITIVE)
    neg_count = sum(1 for w in words if w in _NEGATIVE)
    
    score = pos_count - neg_count
    label = "Neutral"
    if score > 0:
        label = "Positive"
    elif score < 0:
        label = "Negative"
        
    return {
        "label": label,
        "score": score,
        "positive_words": pos_count,
        "negative_words": neg_count
    }
