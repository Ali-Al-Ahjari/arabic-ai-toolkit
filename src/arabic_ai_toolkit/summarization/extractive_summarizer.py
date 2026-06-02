from collections import Counter
from arabic_ai_toolkit.tokenizer.tokenizer import split_sentences, split_words
from arabic_ai_toolkit.stopwords.stopwords import remove_stopwords

def summarize(text: str, num_sentences: int = 2) -> list[str]:
    """
    Summarizes text by scoring sentences based on word frequencies.
    """
    sentences = split_sentences(text)
    if len(sentences) <= num_sentences:
        return sentences
        
    # Calculate word frequencies
    all_words = split_words(text)
    all_words = remove_stopwords(all_words)
    word_freq = Counter(all_words)
    
    if not word_freq:
        return sentences[:num_sentences]
        
    max_freq = max(word_freq.values())
    for word in word_freq:
        word_freq[word] = word_freq[word] / max_freq # Normalize
        
    # Score sentences
    sentence_scores = []
    for i, sentence in enumerate(sentences):
        words = split_words(sentence)
        score = sum(word_freq.get(w, 0) for w in words)
        sentence_scores.append((score, i, sentence))
        
    # Sort by score (descending)
    sentence_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Pick top N
    top_sentences = sentence_scores[:num_sentences]
    
    # Sort back by original index to maintain order
    top_sentences.sort(key=lambda x: x[1])
    
    return [s[2] for s in top_sentences]
