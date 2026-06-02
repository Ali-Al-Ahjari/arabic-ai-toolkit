from arabic_ai_toolkit.correction.auto_correct import correct_common_errors

def test_correct_common_errors() -> None:
    assert correct_common_errors("مرحباً بك ، كيف حالك ؟") == "مرحباً بك، كيف حالك؟"
    assert correct_common_errors("رائععع جدا") == "رائعع جدا"
    assert correct_common_errors("اذهب الية") == "اذهب اليه"
    
    # Pronouns
    assert correct_common_errors("الله علية") == "الله عليه"
    assert correct_common_errors("فية خير") == "فيه خير"
    
    # Advanced
    assert correct_common_errors("انشاء الله خير") == "إن شاء الله خير"
    assert correct_common_errors("هاذا الرجل اللذي جاء") == "هذا الرجل الذي جاء"
