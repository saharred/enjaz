"""
Helper module for handling Arabic text in matplotlib charts.
"""

import arabic_reshaper
from bidi.algorithm import get_display


def fix_arabic_text(text):
    """
    Fix Arabic text for proper display in matplotlib.
    
    Args:
        text: Arabic text string
    
    Returns:
        Properly formatted Arabic text for matplotlib
    """
    if not text:
        return text
    
    # Reshape Arabic text
    reshaped_text = arabic_reshaper.reshape(text)
    
    # Apply bidirectional algorithm
    bidi_text = get_display(reshaped_text)
    
    return bidi_text

