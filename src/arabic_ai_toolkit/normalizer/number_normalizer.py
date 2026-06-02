import re

_EASTERN_TO_WESTERN = {
    '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
    '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
}

def normalize_numbers(text: str) -> str:
    """
    Converts Eastern Arabic numerals (١٢٣) to Western numerals (123).
    Also converts Arabic decimal separators (، or ٫) to a dot (.), but ONLY when between digits.
    """
    for eastern, western in _EASTERN_TO_WESTERN.items():
        text = text.replace(eastern, western)
        
    # Replace Arabic comma '،' or '٫' with dot '.' if it is strictly between two digits
    text = re.sub(r'(?<=\d)[،٫](?=\d)', '.', text)
    return text

def extract_numbers(text: str) -> list[float]:
    """
    Extracts all numeric values from text (integers and floats).
    Automatically normalizes Eastern numerals before extraction.
    """
    text = normalize_numbers(text)
    # Match numbers with optional decimal parts, e.g., 123, 45.67, -8.9
    matches = re.findall(r'-?\b\d+(?:\.\d+)?\b', text)
    return [float(m) for m in matches]
