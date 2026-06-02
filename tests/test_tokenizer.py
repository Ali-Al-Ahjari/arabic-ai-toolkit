from arabic_ai_toolkit.tokenizer.tokenizer import split_words, split_sentences

def test_split_words() -> None:
    assert split_words("أنا أحب البرمجة") == ["أنا", "أحب", "البرمجة"]
    assert split_words("مرحبا، كيف حالك؟") == ["مرحبا", "،", "كيف", "حالك", "؟"]

def test_split_sentences():
    text = "مرحبا. كيف حالك؟ أنا بخير!"
    sentences = split_sentences(text)
    assert sentences == ["مرحبا.", "كيف حالك؟", "أنا بخير!"]

def test_split_sentences_newlines():
    text = "السطر الأول\nالسطر الثاني\r\nالسطر الثالث<br>الرابع"
    sentences = split_sentences(text)
    assert sentences == ["السطر الأول", "السطر الثاني", "السطر الثالث", "الرابع"]
    assert split_sentences("هذه جملة! وهذه أخرى؟ نعم.") == ["هذه جملة!", "وهذه أخرى؟", "نعم."]
