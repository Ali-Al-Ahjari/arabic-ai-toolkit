from arabic_ai_toolkit.tokenizer.tokenizer import split_words, split_sentences

def test_split_words() -> None:
    assert split_words("أنا أحب البرمجة") == ["أنا", "أحب", "البرمجة"]
    assert split_words("مرحبا، كيف حالك؟") == ["مرحبا", "،", "كيف", "حالك", "؟"]

def test_split_sentences() -> None:
    assert split_sentences("مرحبا. كيف حالك؟") == ["مرحبا.", "كيف حالك؟"]
    assert split_sentences("هذه جملة! وهذه أخرى؟ نعم.") == ["هذه جملة!", "وهذه أخرى؟", "نعم."]
