from arabic_ai_toolkit.cleaner.cleaner import clean
from arabic_ai_toolkit.tokenizer.tokenizer import split_words, split_sentences
from arabic_ai_toolkit.normalizer.normalizer import normalize
from arabic_ai_toolkit.keywords.keywords import extract_keywords
from arabic_ai_toolkit.language_detection.language_detection import detect_language
from arabic_ai_toolkit.stemmer.light_stemmer import stem_words
from arabic_ai_toolkit.sentiment.sentiment_analyzer import analyze_sentiment
from arabic_ai_toolkit.summarization.extractive_summarizer import summarize
from arabic_ai_toolkit.correction.auto_correct import correct_common_errors
from arabic_ai_toolkit.language_detection.dialect_detection import detect_dialect

def print_box(title: str, content: str | list | dict) -> None:
    print("\n" + "="*60)
    print(f" 🔹 {title}")
    print("-" * 60)
    if isinstance(content, list):
        for item in content:
            print(f"  - {item}")
    elif isinstance(content, dict):
        for k, v in content.items():
            print(f"  - {k}: {v}")
    else:
        print(f"  {content}")
    print("="*60)

def main() -> None:
    print("\n" + "*"*60)
    print(" "*10 + "مرحباً بك في أداة Arabic AI Toolkit التفاعلية!")
    print(" "*10 + "النسخة المتقدمة (Advanced Features)")
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
            
        # 1. Auto-Correction
        corrected = correct_common_errors(text)
        print_box("التصحيح التلقائي (Auto-Correction)", corrected)
        
        # 2. Cleaning & Normalization
        cleaned = clean(corrected, emojis=True, punctuation=False)
        normalized = normalize(cleaned, ta_marbuta_to_ha=False, hamza=True)
        print_box("التنظيف والتوحيد (Cleaning & Normalization)", normalized)
        
        # 3. Dialect & Language Detection
        lang = detect_language(text)
        if lang == "Arabic":
            dialect = detect_dialect(text)
            print_box("اكتشاف اللغة واللهجة", f"Language: {lang} | Dialect: {dialect}")
        else:
            print_box("اكتشاف اللغة", lang)
        
        # 4. Sentiment Analysis
        sentiment = analyze_sentiment(normalized)
        print_box("تحليل المشاعر (Sentiment Analysis)", f"Label: {sentiment['label']} | Score: {sentiment['score']}")
        
        # 5. Summarization
        sentences = split_sentences(normalized)
        if len(sentences) > 2:
            summary = summarize(normalized, num_sentences=2)
            print_box("التلخيص الاستخراجي (Extractive Summarization)", summary)
        
        # 6. Stemming & Keywords
        words = split_words(normalized)
        stemmed = stem_words(words)
        print_box("المجذّر (Lightweight Stemming - First 10 words)", stemmed[:10])
        
        keywords = extract_keywords(normalized, top_n=5)
        kw_str = " | ".join([f"'{k}' ({v})" for k, v in keywords])
        print_box("أهم الكلمات المفتاحية (Keywords)", kw_str if kw_str else "لا توجد كلمات")

if __name__ == "__main__":
    main()
