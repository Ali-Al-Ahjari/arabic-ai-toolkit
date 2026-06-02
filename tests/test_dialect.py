from arabic_ai_toolkit.language_detection.dialect_detection import detect_dialect

def test_detect_dialect() -> None:
    assert detect_dialect("انا عايز اروح دلوقتي") == "Egyptian"
    assert detect_dialect("بدي اكل هيك شي") == "Levantine"
    assert detect_dialect("وش شكو ماكو") == "Gulf"
    assert detect_dialect("هاد الشي زوين بزاف") == "Maghrebi"
    assert detect_dialect("اللغة العربية الفصحى جميلة") == "MSA/Unknown"
