import argparse
import json

from arabic_ai_toolkit.cleaner.cleaner import clean
from arabic_ai_toolkit.normalizer.normalizer import normalize
from arabic_ai_toolkit.tokenizer.tokenizer import split_words, split_sentences
from arabic_ai_toolkit.keywords.keywords import extract_keywords
from arabic_ai_toolkit.language_detection.language_detection import detect_language
from arabic_ai_toolkit.language_detection.dialect_detection import detect_dialect
from arabic_ai_toolkit.stemmer.light_stemmer import stem_words
from arabic_ai_toolkit.sentiment.sentiment_analyzer import analyze_sentiment
from arabic_ai_toolkit.summarization.extractive_summarizer import summarize
from arabic_ai_toolkit.correction.auto_correct import correct_common_errors

from typing import Any

def main() -> None:
    parser = argparse.ArgumentParser(description="Arabic AI Toolkit CLI")
    parser.add_argument("text", type=str, help="The Arabic text to process")
    parser.add_argument("--action", type=str, required=True, 
                        choices=['clean', 'normalize', 'tokenize', 'sentiment', 'dialect', 'summarize', 'stem', 'keywords', 'correct', 'lang'],
                        help="The operation to perform on the text")
    
    args = parser.parse_args()
    text = args.text
    action = args.action
    
    result: Any = None
    
    if action == 'clean':
        result = clean(text)
    elif action == 'normalize':
        result = normalize(text)
    elif action == 'tokenize':
        result = {"words": split_words(text), "sentences": split_sentences(text)}
    elif action == 'sentiment':
        result = analyze_sentiment(text)
    elif action == 'dialect':
        result = detect_dialect(text)
    elif action == 'summarize':
        result = summarize(text)
    elif action == 'stem':
        result = stem_words(split_words(text))
    elif action == 'keywords':
        result = extract_keywords(text)
    elif action == 'correct':
        result = correct_common_errors(text)
    elif action == 'lang':
        result = detect_language(text)
        
    if isinstance(result, (dict, list)):
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result)

if __name__ == "__main__":
    main()
