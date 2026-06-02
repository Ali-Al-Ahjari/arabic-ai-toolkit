# A basic list of common Arabic stopwords
_STOPWORDS = {
    "في", "من", "على", "إلى", "عن", "ب", "ل", "ك",
    "أن", "إن", "ولا", "لا", "ما", "لم", "لن", "هل",
    "هو", "هي", "هم", "هن", "أنت", "أنا", "نحن",
    "هذا", "هذه", "هؤلاء", "ذلك", "تلك", "الذي", "التي",
    "الذين", "والذي", "كان", "كانت", "يكون", "يا", "أو", "أم", "بل"
}

def get_stopwords() -> set[str]:
    """Returns the set of Arabic stopwords."""
    return _STOPWORDS.copy()

def remove_stopwords(words: list[str]) -> list[str]:
    """Removes stopwords from a list of words."""
    return [word for word in words if word not in _STOPWORDS]
