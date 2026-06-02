from arabic_ai_toolkit.cleaner.cleaner import (
    remove_diacritics,
    remove_tatweel,
    remove_urls,
    remove_punctuation,
    remove_emojis,
    remove_html_tags,
    normalize_spaces,
    clean
)

def test_remove_diacritics() -> None:
    assert remove_diacritics("السَّلَامُ عَلَيْكُمْ") == "السلام عليكم"

def test_remove_tatweel() -> None:
    assert remove_tatweel("مــــرحبــــا") == "مرحبا"

def test_remove_urls() -> None:
    assert remove_urls("زوروا https://example.com") == "زوروا "

def test_remove_html_tags():
    assert remove_html_tags("<p>مرحبا</p> <br>بك") == " مرحبا   بك"

def test_remove_punctuation() -> None:
    assert remove_punctuation("مرحبا!!! 😊، كيف حالك؟") == "مرحبا 😊 كيف حالك"

def test_remove_emojis():
    assert remove_emojis("مرحبا بك 😊") == "مرحبا بك "

def test_normalize_spaces() -> None:
    assert normalize_spaces("أهلا     بكم") == "أهلا بكم"
    assert normalize_spaces("  السلام عليكم  ") == "السلام عليكم"

def test_clean_pipeline() -> None:
    text = "السَّلَامُ عَلَيْكُمْ، مــــرحبــــا!!! 😊 زوروا https://example.com"
    # Default clean: removes diacritics, tatweel, urls, spaces
    assert clean(text) == "السلام عليكم، مرحبا!!! 😊 زوروا"
    
    # Clean all
    assert clean(text, punctuation=True, emojis=True) == "السلام عليكم مرحبا زوروا"
