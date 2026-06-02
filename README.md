# Arabic AI Toolkit 🐪

The ultimate, robust, **rule-based** open-source Arabic Natural Language Processing toolkit for AI builders. 
Process, clean, extract, and analyze Arabic text with lightning speed—**no ML models, no GPUs, and no external APIs required!**

[![CI](https://github.com/Arabic-AI-Community/arabic-ai-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Arabic-AI-Community/arabic-ai-toolkit/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Why Arabic AI Toolkit?
Arabic NLP is notoriously difficult due to complex morphology, dialects, and varied spelling conventions. `arabic-ai-toolkit` solves these challenges natively using advanced rule-based architectures, making it the perfect pre-processing layer before passing data to LLMs or Search Engines.

---

## 🚀 Features (v5.0 Production API Ready)

### 🧹 Cleaning & Normalization
- **Diacritics & Tatweel**: Strips Tashkeel and Kashida.
- **Web Data Cleaner**: Safely removes HTML tags (`<p>`, `<br>`), URLs, emojis, and normalizes whitespaces.
- **Alef/Ya Normalizer**: Unifies `أ, إ, آ` to `ا` and `ى, ئ` to `ي`.
- **Number Normalizer**: Converts Eastern numerals (١٢٣) to Western (123) and handles Arabic decimal commas (`،`).

### ✂️ Core NLP
- **Smart Tokenizer**: Splits words and sentences natively handling `؟` and `\n` boundaries.
- **Light Stemmer**: Strips prefixes (ال, ب, ك, ف) and suffixes (ات, ون, ين) to find the root word.
- **Stopwords**: Standard Arabic stopwords removal.

### 🧠 Advanced Analytics (No ML!)
- **Sentiment Analyzer**: Accurate Positive/Negative scoring with advanced **Negation Context handling** (e.g., understands `ليس جيدا` as negative).
- **Extractive Summarizer**: Summarizes long texts based on tf-idf and root-stemming for high semantic matching.
- **Dialect Detector**: Identifies Egyptian, Levantine, Gulf, and Maghrebi dialects.

### 🏢 Entity Extraction (NER)
- **Generic Organizations**: Detects companies, ministries, banks, universities (e.g., `وزارة الصحة`, `بنك الراجحي`).
- **Dates**: Extracts Gregorian and Hijri text dates (e.g., `15 أيلول 2023`, `1 رمضان 1445`).
- **Money/Currency**: Precisely extracts monetary values (e.g., `150 دولار`, `45.50 ريال`).
- **Locations**: Countries and cities.

### 🛡️ Safety & Corrections
- **Advanced Auto-Correct**: Instantly fixes catastrophic misspellings (`انشاء الله` -> `إن شاء الله`, `اللذي` -> `الذي`).
- **Profanity Filter**: Stemming-aware profanity blocking to catch disguised bad words.

---

## 💻 Installation

```bash
pip install arabic-ai-toolkit
```

## ⚡ Quick Start

### 1. Cleaning Web Data
```python
from arabic_ai_toolkit.cleaner.cleaner import clean

text = "<p>مرحباً بك 😊 في موقعنا https://example.com</p>"
print(clean(text, html_tags=True, emojis=True, urls=True))
# "مرحبا بك في موقعنا"
```

### 2. Entity Extraction (NER)
```python
from arabic_ai_toolkit.ner.entity_extractor import extract_entities

text = "أعلنت وزارة الصحة السعودية عن استثمار 1500 دولار يوم 15 أيلول 2023"
print(extract_entities(text))
# {
#   'locations': ['السعودية'],
#   'organizations': ['وزارة الصحة'],
#   'dates': ['15 أيلول 2023'],
#   'money': ['1500 دولار']
# }
```

### 3. Sentiment Analysis (with Negation)
```python
from arabic_ai_toolkit.sentiment.sentiment_analyzer import analyze_sentiment

print(analyze_sentiment("التطبيق ليس جيدا ولا ممتاز"))
# {'label': 'Negative', 'score': -2, ...}
```

### 4. Advanced Auto-Correction
```python
from arabic_ai_toolkit.correction.auto_correct import correct_common_errors

print(correct_common_errors("هاذا الرجل اللذي جاء انشاء الله فيه خير"))
# "هذا الرجل الذي جاء إن شاء الله فيه خير"
```

---

## 🛠️ CLI Usage
You can run the toolkit directly from your terminal!

```bash
arabic-ai-toolkit --action clean "أهلاً بِكُمْ 😊"
# أهلا بكم

arabic-ai-toolkit --action ner "دفع 50 ريال في الرياض"
# {'locations': ['الرياض'], 'organizations': [], 'dates': [], 'money': ['50 ريال']}
```

## 🤝 Contributing
Contributions are welcome! Please ensure you pass `pytest`, `mypy`, and `ruff` before submitting a PR.

## 📄 License
This project is licensed under the MIT License.

---
## 🔍 Search Keywords (SEO)
Arabic NLP, Arabic Text Processing, Arabic Stemmer, Arabic Sentiment Analysis, Arabic Stopwords, Arabic NER, Arabic Tokenization, Arabic Auto-correct, Arabic Dialect Detection, معالجة اللغات الطبيعية, معالجة اللغة العربية, الذكاء الاصطناعي العربي, تحليل المشاعر العربي, التجذير العربي, استخراج الكيانات العربية, تصحيح إملائي عربي, تلخيص النصوص العربية, مكتبة بايثون لمعالجة النصوص, Python Arabic NLP Library, Arabic Data Cleaning.
