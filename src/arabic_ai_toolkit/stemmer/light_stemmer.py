import re

_PREFIXES = ['وال', 'فال', 'كال', 'بال', 'لل', 'ال']
_SUFFIXES = ['ات', 'ون', 'ين', 'ان', 'ية', 'ها', 'هم', 'هن', 'كم', 'كن', 'نا', 'ي', 'ه', 'ة']

def stem(word: str) -> str:
    original = word
    if len(word) <= 3:
        return word
        
    for pref in _PREFIXES:
        if word.startswith(pref) and len(word) - len(pref) >= 2:
            word = word[len(pref):]
            break
            
    for suff in _SUFFIXES:
        if word.endswith(suff) and len(word) - len(suff) >= 2:
            word = word[:-len(suff)]
            break
            
    if len(word) < 2:
        return original
        
    return word

def stem_words(words: list[str]) -> list[str]:
    return [stem(w) for w in words]
