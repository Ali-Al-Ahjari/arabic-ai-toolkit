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

def display_menu() -> None:
    print("\nاختر العملية التي تريد تنفيذها:")
    print("1. تنفيذ جميع العمليات")
    print("2. التنظيف (Cleaning)")
    print("3. التوحيد (Normalization)")
    print("4. التقسيم (Tokenization)")
    print("5. استخراج الكلمات المفتاحية (Keywords)")
    print("6. كشف اللغة واللهجة (Language & Dialect)")
    print("7. التجذير الخفيف (Stemming)")
    print("8. تحليل المشاعر (Sentiment Analysis)")
    print("9. التلخيص (Summarization)")
    print("10. التصحيح التلقائي (Auto Correction)")
    print("0. خروج")

def main() -> None:
    print("\n" + "*"*60)
    print(" "*10 + "مرحباً بك في أداة Arabic AI Toolkit التفاعلية!")
    print("*"*60 + "\n")
    
    while True:
        display_menu()
        try:
            choice = input("\nرقم العملية: ")
        except EOFError:
            break
            
        if choice == '0' or choice.strip() == 'خروج':
            print("\nإلى اللقاء! 👋\n")
            break
            
        if choice not in [str(i) for i in range(1, 11)]:
            print("الرجاء اختيار رقم صحيح.")
            continue
            
        try:
            text = input("\nأدخل النص الذي تريد معالجته هنا:\n📝 > ")
        except EOFError:
            break
            
        if not text.strip():
            continue
            
        if choice == '1' or choice == '10':
            text = correct_common_errors(text)
            if choice == '10': print_box("التصحيح التلقائي", text)
            
        if choice == '1' or choice == '2':
            cleaned = clean(text, emojis=True, punctuation=False)
            if choice == '2': print_box("التنظيف", cleaned)
            else: text = cleaned
            
        if choice == '1' or choice == '3':
            normalized = normalize(text, ta_marbuta_to_ha=False, hamza=True)
            if choice == '3': print_box("التوحيد", normalized)
            else: text = normalized
            
        if choice == '1' or choice == '4':
            sentences = split_sentences(text)
            words = split_words(text)
            if choice == '4': 
                print_box("الجمل", sentences)
                print_box("الكلمات", words)
                
        if choice == '1' or choice == '5':
            keywords = extract_keywords(text, top_n=5)
            kw_str = " | ".join([f"'{k}' ({v})" for k, v in keywords])
            if choice == '5' or choice == '1': print_box("الكلمات المفتاحية", kw_str if kw_str else "لا توجد")
            
        if choice == '1' or choice == '6':
            lang = detect_language(text)
            if lang == "Arabic":
                dialect = detect_dialect(text)
                print_box("اكتشاف اللغة واللهجة", f"Language: {lang} | Dialect: {dialect}")
            else:
                print_box("اكتشاف اللغة", lang)
                
        if choice == '1' or choice == '7':
            words = split_words(text)
            stemmed = stem_words(words)
            print_box("المجذّر", stemmed[:10])
            
        if choice == '1' or choice == '8':
            sentiment = analyze_sentiment(text)
            print_box("تحليل المشاعر", f"Label: {sentiment['label']} | Score: {sentiment['score']}")
            
        if choice == '1' or choice == '9':
            sentences = split_sentences(text)
            if len(sentences) > 1:
                summary = summarize(text, num_sentences=2)
                print_box("التلخيص", summary)
            elif choice == '9':
                print_box("التلخيص", "النص قصير جداً للتلخيص.")

if __name__ == "__main__":
    main()
