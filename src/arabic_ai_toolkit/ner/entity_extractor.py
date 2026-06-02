import re

_COUNTRIES = {
    "مصر", "السعودية", "الامارات", "الإمارات", "الكويت", "قطر", "البحرين", 
    "عمان", "عُمان", "اليمن", "العراق", "سوريا", "الأردن", "الاردن", "فلسطين", 
    "لبنان", "السودان", "ليبيا", "تونس", "الجزائر", "المغرب", "موريتانيا", "جيبوتي", "الصومال"
}

_CITIES = {
    "القاهرة", "الرياض", "دبي", "أبوظبي", "الكويت", "الدوحة", "المنامة",
    "مسقط", "صنعاء", "بغداد", "دمشق", "عمان", "القدس", "بيروت", "الخرطوم",
    "طرابلس", "تونس", "الجزائر", "الرباط", "نواكشوط", "الإسكندرية", "جدة", "مكة", "المدينة"
}

_ORGANIZATION_KEYWORDS = {"شركة", "مؤسسة", "وزارة", "جامعة", "هيئة", "منظمة", "بنك", "مصرف", "مستشفى", "مدرسة"}

def extract_entities(text: str) -> dict[str, list[str]]:
    """
    Extracts locations (countries, cities), dates, and organizations using rules.
    """
    words = text.split()
    entities: dict[str, list[str]] = {
        "locations": [],
        "organizations": [],
        "dates": []
    }
    
    # 1. Locations
    for word in words:
        clean_word = re.sub(r'^[بالوفك]+', '', word) # Strip common prefixes
        if clean_word in _COUNTRIES or word in _COUNTRIES:
            entities["locations"].append(clean_word if clean_word in _COUNTRIES else word)
        elif clean_word in _CITIES or word in _CITIES:
            entities["locations"].append(clean_word if clean_word in _CITIES else word)
            
    # 2. Organizations
    # Simple rule: If we see an org keyword, capture it and the next 1-2 words
    for i, word in enumerate(words):
        if word in _ORGANIZATION_KEYWORDS:
            org_name = word
            if i + 1 < len(words):
                org_name += " " + words[i+1]
            if i + 2 < len(words) and len(words[i+2]) > 2: # heuristic
                org_name += " " + words[i+2]
            entities["organizations"].append(org_name)
            
    # 3. Dates
    # Match dd-mm-yyyy or yyyy-mm-dd
    numeric_dates = re.findall(r'\b\d{1,4}[-/]\d{1,2}[-/]\d{1,4}\b', text)
    # Match text dates e.g., 12 أكتوبر 2023, 15 شعبان 1445, 1 كانون الأول 2020
    months = (
        r"يناير|فبراير|مارس|أبريل|ابريل|مايو|يونيو|يوليو|أغسطس|اغسطس|سبتمبر|أكتوبر|اكتوبر|نوفمبر|ديسمبر|"
        r"كانون\s+الثاني|شباط|آذار|نيسان|أيار|حزيران|تموز|آب|أيلول|تشرين\s+الأول|تشرين\s+الثاني|كانون\s+الأول|"
        r"محرم|صفر|ربيع\s+الأول|ربيع\s+الآخر|جمادى\s+الأولى|جمادى\s+الآخرة|رجب|شعبان|رمضان|شوال|ذو\s+القعدة|ذو\s+الحجة"
    )
    text_dates = re.findall(rf'\b\d{{1,2}}\s+(?:{months})\s+\d{{4}}\b', text)
    
    entities["dates"].extend(numeric_dates)
    entities["dates"].extend(text_dates)
    
    # Deduplicate
    entities["locations"] = list(set(entities["locations"]))
    entities["organizations"] = list(set(entities["organizations"]))
    entities["dates"] = list(set(entities["dates"]))
    
    return entities
