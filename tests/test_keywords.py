from arabic_ai_toolkit.keywords.keywords import extract_keywords

def test_extract_keywords() -> None:
    text = "الذكاء الاصطناعي هو فرع من علوم الحاسب الذكاء الاصطناعي يتطور"
    keywords = extract_keywords(text, top_n=2)
    # "الذكاء" and "الاصطناعي" should have count 2
    words = [kw[0] for kw in keywords]
    assert "الذكاء" in words
    assert "الاصطناعي" in words
