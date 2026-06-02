from arabic_ai_toolkit.language_detection.language_detection import detect_language

def test_detect_language() -> None:
    assert detect_language("مرحبا بكم") == "Arabic"
    assert detect_language("Hello there") == "English"
    assert detect_language("مرحبا Hello") == "Mixed"
    assert detect_language("12345 @#$") == "Unknown"
