import re
from arabic_ai_toolkit.tokenizer.tokenizer import split_words
from arabic_ai_toolkit.stemmer.light_stemmer import stem

# A basic conceptual list of inappropriate words (kept light for demonstration)
_PROFANITY_LIST = {
    "غبي", "حمار", "كلب", "تافه", "حقير", "سافل", "قذر", "احمق", "أحمق", "ملعون", "زفت"
}

def has_profanity(text: str) -> bool:
    """
    Checks if the text contains any profanity.
    """
    words = split_words(text)
    for word in words:
        clean_word = re.sub(r'[^\w\s]', '', word)
        if clean_word.startswith('يا') and len(clean_word) > 2:
            clean_word = clean_word[2:]
        if clean_word in _PROFANITY_LIST or stem(clean_word) in _PROFANITY_LIST:
            return True
    return False

def censor_text(text: str, replacer: str = "***") -> str:
    """
    Replaces profane words with a replacer string.
    """
    words = text.split()
    censored_words = []
    
    for word in words:
        # Strip punctuation to check the core word
        clean_word = re.sub(r'[^\w\s]', '', word)
        is_ya_prefixed = clean_word.startswith('يا') and len(clean_word) > 2
        test_word = clean_word[2:] if is_ya_prefixed else clean_word
        
        if test_word in _PROFANITY_LIST or stem(test_word) in _PROFANITY_LIST:
            # Replace the word but keep length? For simplicity just use replacer.
            censored_words.append(replacer)
        else:
            censored_words.append(word)
            
    return " ".join(censored_words)
