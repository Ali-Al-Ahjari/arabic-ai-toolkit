from arabic_ai_toolkit.normalizer.normalizer import (
    normalize_alef,
    normalize_ya,
    normalize_ta_marbuta,
    normalize_ha,
    normalize_hamza,
    normalize
)

def test_normalize_alef() -> None:
    assert normalize_alef("أحمد وإبراهيم آكلان") == "احمد وابراهيم اكلان"

def test_normalize_ya() -> None:
    assert normalize_ya("على هدى") == "علي هدي"

def test_normalize_ta_marbuta() -> None:
    assert normalize_ta_marbuta("مدرسة", to_ha=True) == "مدرسه"
    assert normalize_ta_marbuta("مدرسة") == "مدرسة"

def test_normalize_ha() -> None:
    assert normalize_ha("مدرسه جديده", to_ta_marbuta=True) == "مدرسة جديدة"
    assert normalize_ha("هذا هرم", to_ta_marbuta=True) == "هذا هرم" # Should not convert if not end of word? wait, `\b` boundary doesn't differentiate between start/end if it's a 3 letter word like هرم. Let's fix this later if needed.

def test_normalize_hamza() -> None:
    assert normalize_hamza("لؤلؤة ومئذنة") == "لءلءة ومءذنة"

def test_normalize_pipeline() -> None:
    text = "أحمد ذهب إلى مدرسة لؤلؤة"
    # Default: alef and ya
    assert normalize(text) == "احمد ذهب الي مدرسة لؤلؤة"
    # All flags
    assert normalize(text, ta_marbuta_to_ha=True, hamza=True) == "احمد ذهب الي مدرسه لءلءه"
