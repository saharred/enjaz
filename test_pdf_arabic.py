#!/usr/bin/env python3
"""
Test script to verify Arabic text rendering in PDF exports.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from enjaz.pdf_fonts import register_arabic_fonts, AMIRI_REGULAR, AMIRI_BOLD
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
import arabic_reshaper
from bidi.algorithm import get_display


def reshape_arabic(text):
    """Reshape Arabic text for PDF display."""
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)


def test_pdf_arabic():
    """Test PDF generation with Arabic text."""
    print("Testing PDF Arabic font rendering...")
    
    # Register Arabic fonts
    register_arabic_fonts()
    print(f"✓ Arabic fonts registered: {AMIRI_REGULAR}, {AMIRI_BOLD}")
    
    # Create test PDF
    output_path = Path(__file__).parent / "test_arabic_output.pdf"
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Title style with Arabic font
    title_style = ParagraphStyle(
        'ArabicTitle',
        parent=styles['Title'],
        alignment=TA_CENTER,
        fontSize=18,
        textColor=colors.HexColor('#6d3a46'),
        spaceAfter=20,
        fontName=AMIRI_BOLD
    )
    
    # Heading style with Arabic font
    heading_style = ParagraphStyle(
        'ArabicHeading',
        parent=styles['Heading1'],
        alignment=TA_RIGHT,
        fontSize=14,
        textColor=colors.HexColor('#6d3a46'),
        spaceAfter=10,
        fontName=AMIRI_BOLD
    )
    
    # Body style with Arabic font
    body_style = ParagraphStyle(
        'ArabicBody',
        parent=styles['BodyText'],
        alignment=TA_RIGHT,
        fontSize=11,
        spaceAfter=10,
        fontName=AMIRI_REGULAR
    )
    
    # Add test content
    title_text = reshape_arabic("اختبار عرض النص العربي في ملفات PDF")
    elements.append(Paragraph(title_text, title_style))
    elements.append(Spacer(1, 1*cm))
    
    heading_text = reshape_arabic("العنوان الرئيسي بخط Amiri Bold")
    elements.append(Paragraph(heading_text, heading_style))
    elements.append(Spacer(1, 0.5*cm))
    
    body_text = reshape_arabic(
        "هذا نص تجريبي بالخط العربي Amiri Regular. "
        "يجب أن يظهر النص العربي بشكل واضح وصحيح، "
        "وليس كمربعات سوداء. إذا ظهر النص بشكل صحيح، "
        "فهذا يعني أن الخط العربي يعمل بشكل سليم."
    )
    elements.append(Paragraph(body_text, body_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Add numbers test
    numbers_text = reshape_arabic("الأرقام: ١٢٣٤٥٦٧٨٩٠ | 0123456789")
    elements.append(Paragraph(numbers_text, body_style))
    
    # Build PDF
    doc.build(elements)
    
    print(f"✓ PDF created successfully: {output_path}")
    print(f"✓ File size: {output_path.stat().st_size} bytes")
    print("\nPlease open the PDF file to verify that Arabic text displays correctly.")
    print("If you see clear Arabic text (not black squares), the fix is successful!")
    
    return output_path


if __name__ == "__main__":
    try:
        output = test_pdf_arabic()
        print(f"\n✅ Test completed successfully!")
        print(f"📄 Output file: {output}")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

