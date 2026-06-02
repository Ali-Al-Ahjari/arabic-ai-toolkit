from arabic_ai_toolkit.summarization.extractive_summarizer import summarize

def test_summarize() -> None:
    text = "الذكاء الاصطناعي هو فرع من علوم الحاسب. الذكاء الاصطناعي يتطور بسرعة مذهلة. هذه الجملة ليست مهمة جدا. نحن نحب الذكاء الاصطناعي."
    summary = summarize(text, num_sentences=2)
    assert len(summary) == 2
    assert "الذكاء الاصطناعي يتطور بسرعة مذهلة." in summary
