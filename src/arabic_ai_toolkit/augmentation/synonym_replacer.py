import random

_SYNONYMS = {
    "جيد": ["ممتاز", "رائع", "حسن"],
    "سيء": ["رديء", "قبيح", "غير جيد"],
    "كبير": ["ضخم", "هائل", "عظيم", "شاسع"],
    "صغير": ["ضئيل", "دقيق", "قليل"],
    "سعيد": ["مسرور", "فرحان", "مبتهج"],
    "حزين": ["مكتئب", "تعيس", "مهموم"],
    "جميل": ["فاتن", "رائع", "بديع", "وسيم", "جذاب"],
    "سريع": ["عاجل", "خاطف", "مسرع"],
    "بطيء": ["متثاقل", "متأخر"],
    "كثير": ["وفير", "عديد", "غزير"],
    "قليل": ["نادر", "شحيح", "بسيط"],
    "مهم": ["ضروري", "حيوي", "أساسي"],
    "سهل": ["يسير", "بسيط", "هين"],
    "صعب": ["عسير", "شاق", "معقد"]
}

_PREFIXES = sorted(['وال', 'فال', 'كال', 'بال', 'لل', 'ال', 'ب', 'ف', 'ك', 'و'], key=len, reverse=True)

def _get_synonym_with_prefix(word: str) -> str | None:
    if word in _SYNONYMS:
        return random.choice(_SYNONYMS[word])
        
    for p in _PREFIXES:
        if word.startswith(p) and len(word) > len(p) + 2:
            base = word[len(p):]
            if base in _SYNONYMS:
                return p + random.choice(_SYNONYMS[base])
    return None

def augment_text(text: str, n_variations: int = 3) -> list[str]:
    """
    Augments text by replacing words with their synonyms.
    Generates up to n_variations unique variations.
    """
    words = text.split()
    variations: set[str] = set()
    
    # Try to generate variations
    attempts = 0
    max_attempts = n_variations * 10
    
    while len(variations) < n_variations and attempts < max_attempts:
        new_words = []
        changed = False
        for word in words:
            synonym = _get_synonym_with_prefix(word)
            if synonym and random.random() > 0.3: # 70% chance to replace if synonym exists
                new_words.append(synonym)
                changed = True
            else:
                new_words.append(word)
                
        new_text = " ".join(new_words)
        if changed and new_text != text:
            variations.add(new_text)
            
        attempts += 1
        
    return list(variations)
