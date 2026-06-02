from arabic_ai_toolkit.cleaner.cleaner import clean
from arabic_ai_toolkit.tokenizer.tokenizer import split_words
from arabic_ai_toolkit.normalizer.normalizer import normalize
from arabic_ai_toolkit.keywords.keywords import extract_keywords
from arabic_ai_toolkit.language_detection.language_detection import detect_language

def main() -> None:
    text = "مــــرحبــــا!!! 😊 زوروا موقعنا https://example.com، الذكاء الاصطناعي يتطور بسرعة."
    print("Original:", text)
    
    # Language Detection
    lang = detect_language(text)
    print("Language:", lang)
    
    # Clean
    cleaned = clean(text, emojis=True)
    print("Cleaned:", cleaned)
    
    # Normalize
    normalized = normalize(cleaned)
    print("Normalized:", normalized)
    
    # Tokenize
    words = split_words(normalized)
    print("Tokens:", words)
    
    # Keywords
    kws = extract_keywords(normalized, top_n=2)
    print("Keywords:", kws)

if __name__ == "__main__":
    main()
