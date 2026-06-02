from typing import Any
from arabic_ai_toolkit.tokenizer.tokenizer import split_words
from arabic_ai_toolkit.normalizer.normalizer import normalize

# Very basic lexicons
_POSITIVE = {"ممتاز", "رائع", "جيد", "جيدا", "جميل", "عظيم", "مذهل", "احب", "سعيد", "رائعة", "ابداع", "ممتع"}
_NEGATIVE = {"سيء", "سيئا", "حزين", "قبيح", "رديء", "اكره", "مزعج", "فاشل", "ممل", "غبي", "ضعيف"}
_NEGATION = {"لا", "لم", "لن", "ليس", "ما", "غير", "مش", "ولا", "وما", "ولم", "وليس", "ولن"}

def analyze_sentiment(text: str) -> dict[str, Any]:
    """
    Returns sentiment scores based on word counts.
    """
    words = split_words(normalize(text))
    pos_count = 0
    neg_count = 0
    
    for i, w in enumerate(words):
        is_negated = i > 0 and words[i-1] in _NEGATION
        if w in _POSITIVE:
            if is_negated:
                neg_count += 1
            else:
                pos_count += 1
        elif w in _NEGATIVE:
            if is_negated:
                pos_count += 1
            else:
                neg_count += 1
    
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
