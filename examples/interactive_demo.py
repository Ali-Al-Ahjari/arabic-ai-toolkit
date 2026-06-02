from arabic_ai_toolkit.cleaner.cleaner import clean
from arabic_ai_toolkit.tokenizer.tokenizer import split_words, split_sentences
from arabic_ai_toolkit.normalizer.normalizer import normalize
from arabic_ai_toolkit.keywords.keywords import extract_keywords
from arabic_ai_toolkit.language_detection.language_detection import detect_language
import sys

def print_box(title: str, content: str | list) -> None:
    print("\n" + "="*60)
    print(f" 🔹 {title}")
    print("-" * 60)
    if isinstance(content, list):
        for item in content:
            print(f"  - {item}")
    else:
        print(f"  {content}")
    print("="*60)

def main() -> None:
    print("\n" + "*"*60)
    print(" "*10 + "مرحباً بك في أداة Arabic AI Toolkit التفاعلية!")
    print(" "*10 + "اكتب 'خروج' لإنهاء البرنامج في أي وقت.")
    print("*"*60 + "\n")
    
    while True:
        try:
            text = input("\nأدخل النص الذي تريد معالجته هنا:\n📝 > ")
        except EOFError:
            break
            
        if text.strip() == 'خروج':
            print("\nإلى اللقاء! 👋\n")
            break
        if not text.strip():
            continue
            
        # 1. Language Detection
        lang = detect_language(text)
        print_box("اكتشاف اللغة (Language Detection)", lang)
        
        # 2. Cleaning
        cleaned = clean(text, emojis=True, punctuation=False)
        print_box("النص بعد التنظيف (إزالة التشكيل، الروابط، التطويل)", cleaned)
        
        # 3. Normalization
        normalized = normalize(cleaned, ta_marbuta_to_ha=False, hamza=True)
        print_box("النص بعد التوحيد (توحيد الألف والياء والهمزات)", normalized)
        
        # 4. Tokenization (Sentences)
        sentences = split_sentences(normalized)
        print_box("تقسيم الجمل (Sentence Tokenization)", sentences)
        
        # 5. Tokenization (Words)
        words = split_words(normalized)
        print_box("تقسيم الكلمات (Word Tokenization)", words)
        
        # 6. Keywords Extraction
        keywords = extract_keywords(normalized, top_n=5)
        kw_str = " | ".join([f"'{k}' (تكررت {v} مرات)" for k, v in keywords])
        print_box("أهم الكلمات المفتاحية (Keyword Extraction)", kw_str if kw_str else "لا توجد كلمات")

if __name__ == "__main__":
    main()
