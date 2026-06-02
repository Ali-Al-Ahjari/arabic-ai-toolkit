from arabic_ai_toolkit.sentiment.sentiment_analyzer import analyze_sentiment

def test_analyze_sentiment() -> None:
    res1 = analyze_sentiment("هذا منتج رائع وممتاز جدا")
    assert res1["label"] == "Positive"
    
    res2 = analyze_sentiment("تطبيق سيء وفاشل وممل")
    assert res2["label"] == "Negative"
    
    res3 = analyze_sentiment("سيارة عادية")
    assert res3["label"] == "Neutral"

def test_analyze_sentiment_negation():
    text = "التطبيق ليس جيدا ولا ممتاز"
    result = analyze_sentiment(text)
    assert result["label"] == "Negative"
    assert result["score"] < 0
