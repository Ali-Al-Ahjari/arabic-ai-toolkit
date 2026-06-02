import gradio as gr
from arabic_ai_toolkit.cleaner.cleaner import clean
from arabic_ai_toolkit.normalizer.normalizer import normalize
from arabic_ai_toolkit.tokenizer.tokenizer import split_words
from arabic_ai_toolkit.keywords.keywords import extract_keywords
from arabic_ai_toolkit.language_detection.language_detection import detect_language
from arabic_ai_toolkit.language_detection.dialect_detection import detect_dialect
from arabic_ai_toolkit.stemmer.light_stemmer import stem_words
from arabic_ai_toolkit.sentiment.sentiment_analyzer import analyze_sentiment
from arabic_ai_toolkit.summarization.extractive_summarizer import summarize
from arabic_ai_toolkit.correction.auto_correct import correct_common_errors

def process_text(text: str, operations: list[str]) -> str:
    if not text.strip():
        return "الرجاء إدخال نص أولاً."
        
    results = []
    current_text = text
    
    if "Auto-Correction" in operations:
        current_text = correct_common_errors(current_text)
        results.append(f"✅ التصحيح التلقائي:\n{current_text}")
        
    if "Clean" in operations:
        current_text = clean(current_text, emojis=True, punctuation=False)
        results.append(f"🧹 التنظيف:\n{current_text}")
        
    if "Normalize" in operations:
        current_text = normalize(current_text, ta_marbuta_to_ha=False, hamza=True)
        results.append(f"📏 التوحيد:\n{current_text}")
        
    if "Language/Dialect" in operations:
        lang = detect_language(text)
        if lang == "Arabic":
            dialect = detect_dialect(text)
            results.append(f"🌍 اللغة: {lang} | اللهجة: {dialect}")
        else:
            results.append(f"🌍 اللغة: {lang}")
            
    if "Sentiment" in operations:
        sentiment = analyze_sentiment(current_text)
        results.append(f"🎭 المشاعر: {sentiment['label']} (Score: {sentiment['score']})")
        
    if "Summarize" in operations:
        summary = summarize(current_text, num_sentences=2)
        results.append(f"📄 التلخيص:\n" + "\n".join(summary))
        
    if "Tokenize" in operations:
        words = split_words(current_text)
        results.append(f"✂️ الكلمات ({len(words)}):\n{words}")
        
    if "Keywords" in operations:
        kws = extract_keywords(current_text, top_n=5)
        kw_str = " | ".join([f"{k} ({v})" for k, v in kws])
        results.append(f"🔑 الكلمات المفتاحية:\n{kw_str if kw_str else 'لا توجد'}")
        
    if "Stem" in operations:
        words = split_words(current_text)
        stemmed = stem_words(words)
        results.append(f"🌱 التجذير:\n{stemmed[:15]}...")

    if not operations:
        return "يرجى اختيار عملية واحدة على الأقل من القائمة."
        
    return "\n\n".join(results)

# Create a beautiful and clean UI with Soft theme
with gr.Blocks(title="Arabic AI Toolkit", theme=gr.themes.Soft(primary_hue="blue")) as demo:
    gr.Markdown("# 🚀 Arabic AI Toolkit - Studio")
    gr.Markdown("واجهة رسومية أنيقة وبسيطة لتجربة أدوات معالجة اللغة العربية.")
    
    with gr.Row():
        with gr.Column(scale=1):
            text_input = gr.Textbox(
                label="أدخل النص العربي هنا", 
                lines=10, 
                placeholder="اكتب نصاً أو الصق مقالاً طويلاً هنا لتجربة الأداة..."
            )
            operations = gr.CheckboxGroup(
                ["Auto-Correction", "Clean", "Normalize", "Language/Dialect", "Sentiment", "Summarize", "Tokenize", "Keywords", "Stem"],
                label="اختر العمليات التي تريد تنفيذها",
                value=["Auto-Correction", "Clean", "Normalize", "Language/Dialect", "Sentiment", "Keywords"]
            )
            submit_btn = gr.Button("معالجة النص ✨", variant="primary")
            
        with gr.Column(scale=1):
            output_display = gr.Textbox(label="النتائج", lines=18, interactive=False)
            
    submit_btn.click(fn=process_text, inputs=[text_input, operations], outputs=output_display)

if __name__ == "__main__":
    demo.launch(server_port=7860, show_api=False)
