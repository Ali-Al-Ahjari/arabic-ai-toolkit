from arabic_ai_toolkit.stemmer.light_stemmer import stem

def test_stem() -> None:
    assert stem("المدرسون") == "مدرس"
    assert stem("بالسيارة") == "سيار"
    assert stem("كتابهم") == "كتاب"
