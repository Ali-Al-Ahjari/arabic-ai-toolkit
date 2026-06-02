from arabic_ai_toolkit.cleaner.profanity_filter import has_profanity, censor_text

def test_has_profanity():
    assert has_profanity("انت شخص غبي جدا")
    assert not has_profanity("انت شخص ذكي جدا")

def test_censor_text():
    assert censor_text("يا كلب لماذا فعلت هذا؟") == "يا *** لماذا فعلت هذا؟"
    assert censor_text("الطقس جميل اليوم") == "الطقس جميل اليوم"
