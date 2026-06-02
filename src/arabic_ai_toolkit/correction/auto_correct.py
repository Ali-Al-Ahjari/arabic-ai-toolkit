import re

def correct_common_errors(text: str) -> str:
    """
    Fixes very common typos in Arabic text using regex.
    """
    # Fix repeated characters > 2 times (e.g. مرررحبا -> مرحبا)
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)
    
    # Fix spaces before punctuation
    text = re.sub(r'\s+([،.؛؟!])', r'\1', text)
    
    # Very naive fix for 'ة' instead of 'ه' in pronouns like (عليه، فيه) which are often mistyped (علية، فية)
    text = re.sub(r'\b(علي|في|إلي|الي|عن|من)ة\b', r'\1ه', text)
    
    return text
