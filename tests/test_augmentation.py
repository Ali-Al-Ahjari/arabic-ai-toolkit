from arabic_ai_toolkit.augmentation.synonym_replacer import augment_text

def test_augment_text():
    text = "الطقس جميل جدا اليوم"
    variations = augment_text(text, n_variations=3)
    
    # We should get some variations since 'جميل' is in synonyms
    assert len(variations) > 0
    assert text not in variations
    
    # At least one word in variations should be different from original
    original_words = set(text.split())
    for var in variations:
        var_words = set(var.split())
        assert original_words != var_words

def test_augment_with_prefixes():
    text = "رأيت الرجل والجميل"
    variations = augment_text(text, n_variations=1)
    if variations:
        assert "والجميل" not in variations[0]
        # Depending on synonym, it should retain the prefix "وال"
        # E.g. والوسيم, والرائع
        assert any(var.startswith("رأيت الرجل وال") for var in variations)

def test_augment_no_synonyms():
    text = "هذا نص عادي"
    variations = augment_text(text, n_variations=3)
    assert len(variations) == 0
