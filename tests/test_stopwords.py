from arabic_ai_toolkit.stopwords.stopwords import get_stopwords, remove_stopwords

def test_get_stopwords() -> None:
    stopwords = get_stopwords()
    assert "في" in stopwords
    assert "على" in stopwords

def test_remove_stopwords() -> None:
    words = ["أنا", "أدرس", "في", "الجامعة"]
    filtered = remove_stopwords(words)
    assert filtered == ["أدرس", "الجامعة"]
