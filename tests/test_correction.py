from arabic_ai_toolkit.correction.auto_correct import correct_common_errors

def test_correct_common_errors() -> None:
    assert correct_common_errors("مرحباً بك ، كيف حالك ؟") == "مرحباً بك، كيف حالك؟"
    assert correct_common_errors("رائععع جدا") == "رائعع جدا"
    assert correct_common_errors("اذهب الية") == "اذهب اليه"
