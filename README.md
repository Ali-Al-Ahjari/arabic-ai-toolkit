# Arabic AI Toolkit 🐪

The open-source Arabic preprocessing toolkit for builders. Make dealing with Arabic text easier, faster, and more consistent.

## Features
- 🧹 **Cleaner**: Remove diacritics, tatweel, symbols, and links.
- 📏 **Normalizer**: Normalize Alef, Ya, and spaces.
- ✂️ **Tokenizer**: Fast word and sentence splitting.
- 🛑 **Stopwords**: Standard Arabic stopwords removal.
- 🔑 **Keywords**: Lightweight keyword extraction.
- 🌐 **Language Detection**: Detect Arabic, English, and Mixed text.

## Installation
```bash
pip install arabic-ai-toolkit
```

## Quick Start
```python
from arabic_ai_toolkit.cleaner import remove_diacritics

text = "السَّلَامُ عَلَيْكُمْ"
clean_text = remove_diacritics(text)
print(clean_text) # السلام عليكم
```

## License
MIT License
