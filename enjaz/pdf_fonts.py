"""
PDF Fonts Module for Enjaz Application.
Registers Arabic fonts for proper PDF rendering.
"""

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import os


# Font paths
FONTS_DIR = Path(__file__).parent.parent / "fonts"

# Font names
AMIRI_REGULAR = "Amiri-Regular"
AMIRI_BOLD = "Amiri-Bold"
AMIRI_ITALIC = "Amiri-Italic"
AMIRI_BOLD_ITALIC = "Amiri-BoldItalic"


def register_arabic_fonts():
    """
    Register Arabic fonts for ReportLab PDF generation.
    
    This function registers the Amiri font family which supports Arabic text.
    Call this function once at the start of the application.
    """
    try:
        # Register Amiri Regular
        amiri_regular_path = FONTS_DIR / "Amiri-Regular.ttf"
        if amiri_regular_path.exists():
            pdfmetrics.registerFont(TTFont(AMIRI_REGULAR, str(amiri_regular_path)))
        
        # Register Amiri Bold
        amiri_bold_path = FONTS_DIR / "Amiri-Bold.ttf"
        if amiri_bold_path.exists():
            pdfmetrics.registerFont(TTFont(AMIRI_BOLD, str(amiri_bold_path)))
        
        # Register Amiri Italic
        amiri_italic_path = FONTS_DIR / "Amiri-Italic.ttf"
        if amiri_italic_path.exists():
            pdfmetrics.registerFont(TTFont(AMIRI_ITALIC, str(amiri_italic_path)))
        
        # Register Amiri Bold Italic
        amiri_bold_italic_path = FONTS_DIR / "Amiri-BoldItalic.ttf"
        if amiri_bold_italic_path.exists():
            pdfmetrics.registerFont(TTFont(AMIRI_BOLD_ITALIC, str(amiri_bold_italic_path)))
        
        return True
    
    except Exception as e:
        print(f"Warning: Could not register Arabic fonts: {e}")
        return False


def get_arabic_font_name(bold=False, italic=False):
    """
    Get the appropriate Arabic font name based on style.
    
    Args:
        bold: Use bold font
        italic: Use italic font
    
    Returns:
        str: Font name
    """
    if bold and italic:
        return AMIRI_BOLD_ITALIC
    elif bold:
        return AMIRI_BOLD
    elif italic:
        return AMIRI_ITALIC
    else:
        return AMIRI_REGULAR


def is_arabic_font_available():
    """
    Check if Arabic fonts are available.
    
    Returns:
        bool: True if fonts are available, False otherwise
    """
    amiri_regular_path = FONTS_DIR / "Amiri-Regular.ttf"
    return amiri_regular_path.exists()


# Auto-register fonts on module import
register_arabic_fonts()

