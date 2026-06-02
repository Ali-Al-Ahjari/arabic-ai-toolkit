from arabic_ai_toolkit.normalizer.number_normalizer import normalize_numbers, extract_numbers

def test_normalize_numbers():
    assert normalize_numbers("رقمي هو ٠١٢٣٤٥٦٧٨٩") == "رقمي هو 0123456789"
    assert normalize_numbers("التاريخ ٢٠٢٣") == "التاريخ 2023"

def test_extract_numbers():
    assert extract_numbers("لدي ١٥ تفاحة و 3.5 برتقالات") == [15.0, 3.5]
    assert extract_numbers("درجة الحرارة -٥.٢") == [-5.2]
