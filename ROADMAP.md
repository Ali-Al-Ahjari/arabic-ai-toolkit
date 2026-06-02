# Arabic AI Toolkit - Detailed Roadmap

This roadmap outlines the journey from our core MVP (v1.0) to an advanced, industry-leading Arabic NLP library.

## Phase 1: Core Features (v1.0) - [COMPLETED]
- [x] Text Cleaning (Diacritics, Tatweel, URLs, Emojis)
- [x] Text Normalization (Alef, Ya, Ta Marbuta, Spaces)
- [x] Tokenization (Sentences and Words)
- [x] Stopwords Management
- [x] Basic Keyword Extraction
- [x] Language Detection Heuristics

## Phase 2: Advanced NLP Features (The Next 10 Big Features)
1. **Stemming & Lemmatization (الرد إلى الجذر والأصل)**
   - Extracting the root word (e.g., "مدرسون" -> "درس") using rule-based and statistical algorithms.
2. **Dialect Detection & Processing (كشف اللهجات ومعالجتها)**
   - Identifying and mapping dialects (Egyptian, Gulf, Levantine, Maghrebi) to Modern Standard Arabic (MSA).
3. **Diacritization Engine (التشكيل الآلي)**
   - Automatically restoring missing diacritics (Harakat) using lightweight transformer models to resolve ambiguities.
4. **Named Entity Recognition - NER (استخراج الكيانات المسماة)**
   - Identifying people, locations, organizations, and dates natively in Arabic text.
5. **Sentiment Analysis (تحليل المشاعر)**
   - Detecting positive, negative, and neutral sentiments tailored to Arabic culture and slang.
6. **Spell Checker & Auto-Correction (التدقيق الإملائي)**
   - Fixing common typos contextually (e.g., differentiating between ة and ه, ض and ظ).
7. **Part-of-Speech Tagging - POS (التحليل الصرفي والنحوي)**
   - Tagging verbs, nouns, adjectives, and prepositions according to Arabic grammatical rules.
8. **Text Summarization (التلخيص الآلي)**
   - Extractive algorithms to summarize long Arabic documents and news articles.
9. **Semantic Embeddings for RAG (التضمين الدلالي)**
   - Providing localized vector embeddings optimized for Arabic to use in Retrieval-Augmented Generation (RAG).
10. **Data Augmentation (تكبير البيانات وتوليد المرادفات)**
    - Paraphrasing sentences and replacing words with synonyms to augment training datasets for ML models.
