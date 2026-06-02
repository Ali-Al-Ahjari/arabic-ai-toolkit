from arabic_ai_toolkit.ner.entity_extractor import extract_entities

def test_extract_locations():
    text = "سافرت من القاهرة إلى السعودية"
    entities = extract_entities(text)
    assert "القاهرة" in entities["locations"]
    assert "السعودية" in entities["locations"]

def test_extract_organizations():
    text = "أعلنت شركة أبل عن أرباحها"
    entities = extract_entities(text)
    assert any("شركة أبل" in org for org in entities["organizations"])

def test_extract_dates():
    text = "تاريخ اليوم هو 12 أكتوبر 2023 وفي الرقم 12-10-2023"
    entities = extract_entities(text)
    assert "12-10-2023" in entities["dates"]
    assert "12 أكتوبر 2023" in entities["dates"]

def test_extract_eastern_and_hijri_dates():
    text = "بدأ الفصل في 15 أيلول 2023 وانتهى في 1 رمضان 1445"
    entities = extract_entities(text)
    assert "15 أيلول 2023" in entities["dates"]
    assert "1 رمضان 1445" in entities["dates"]
