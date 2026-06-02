import re

# Normalization maps
_ALEF_REGEX = re.compile(r'[أإآ]')
_YA_REGEX = re.compile(r'[ىي]')
_TA_MARBUTA_REGEX = re.compile(r'ة')
_HA_REGEX = re.compile(r'ه')
_HAMZA_REGEX = re.compile(r'[ؤئ]')

def normalize_alef(text: str) -> str:
    """Normalizes all forms of Alef (أ, إ, آ) to a bare Alef (ا)."""
    return _ALEF_REGEX.sub('ا', text)

def normalize_ya(text: str) -> str:
    """Normalizes Alef Maksura (ى) and Ya (ي) to Ya (ي)."""
    return _YA_REGEX.sub('ي', text)

def normalize_ta_marbuta(text: str, to_ha: bool = False) -> str:
    """Normalizes Ta Marbuta (ة) to Ha (ه) if to_ha is True, else does nothing (or can be customized)."""
    if to_ha:
        return _TA_MARBUTA_REGEX.sub('ه', text)
    return text

def normalize_ha(text: str, to_ta_marbuta: bool = False) -> str:
    """Normalizes Ha (ه) at the end of words to Ta Marbuta (ة) if to_ta_marbuta is True."""
    if to_ta_marbuta:
        # Only replace word-final ha
        return re.sub(r'ه\b', 'ة', text)
    return text

def normalize_hamza(text: str) -> str:
    """Normalizes Hamza forms (ؤ, ئ) to standalone Hamza (ء)."""
    return _HAMZA_REGEX.sub('ء', text)

def normalize(text: str,
              alef: bool = True,
              ya: bool = True,
              ta_marbuta_to_ha: bool = False,
              ha_to_ta_marbuta: bool = False,
              hamza: bool = False) -> str:
    """
    Normalizes Arabic text according to the provided flags.
    By default, normalizes Alef and Ya.
    """
    if alef:
        text = normalize_alef(text)
    if ya:
        text = normalize_ya(text)
    if ta_marbuta_to_ha:
        text = normalize_ta_marbuta(text, to_ha=True)
    if ha_to_ta_marbuta:
        text = normalize_ha(text, to_ta_marbuta=True)
    if hamza:
        text = normalize_hamza(text)
    
    return text
