#!/usr/bin/env python3
"""
Comprehensive PDF Generation Test Script
Tests Arabic font rendering with detailed debugging information
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("PDF Arabic Font Test - Comprehensive Diagnostics")
print("=" * 60)

# Step 1: Check font files
print("\n1. Checking font files...")
fonts_dir = Path(__file__).parent / "fonts"
print(f"   Fonts directory: {fonts_dir}")
print(f"   Directory exists: {fonts_dir.exists()}")

if fonts_dir.exists():
    font_files = list(fonts_dir.glob("*.ttf"))
    print(f"   Found {len(font_files)} font files:")
    for font in font_files:
        print(f"      - {font.name} ({font.stat().st_size} bytes)")
else:
    print("   ❌ ERROR: Fonts directory not found!")
    sys.exit(1)

# Step 2: Import and register fonts
print("\n2. Importing PDF fonts module...")
try:
    from enjaz.pdf_fonts import (
        register_arabic_fonts, 
        AMIRI_REGULAR, 
        AMIRI_BOLD,
        is_arabic_font_available
    )
    print("   ✓ Module imported successfully")
    print(f"   AMIRI_REGULAR: {AMIRI_REGULAR}")
    print(f"   AMIRI_BOLD: {AMIRI_BOLD}")
    print(f"   Fonts available: {is_arabic_font_available()}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 3: Check ReportLab font registration
print("\n3. Checking ReportLab font registration...")
try:
    from reportlab.pdfbase import pdfmetrics
    
    registered_fonts = pdfmetrics.getRegisteredFontNames()
    print(f"   Total registered fonts: {len(registered_fonts)}")
    
    amiri_fonts = [f for f in registered_fonts if 'Amiri' in f]
    if amiri_fonts:
        print(f"   ✓ Amiri fonts registered: {amiri_fonts}")
    else:
        print("   ⚠️  WARNING: No Amiri fonts found in registered fonts")
        print(f"   Registered fonts: {registered_fonts[:10]}...")
        
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Step 4: Create test PDF
print("\n4. Creating test PDF...")
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
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
    
    output_path = Path(__file__).parent / "test_pdf_comprehensive.pdf"
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
    
    # Test 1: Title with AMIRI_BOLD
    print("   Creating title style with AMIRI_BOLD...")
    title_style = ParagraphStyle(
        'ArabicTitle',
        parent=styles['Title'],
        alignment=TA_CENTER,
        fontSize=18,
        textColor=colors.HexColor('#6d3a46'),
        spaceAfter=20,
        fontName=AMIRI_BOLD
    )
    
    title_text = reshape_arabic("اختبار شامل لعرض النص العربي في ملفات PDF")
    elements.append(Paragraph(title_text, title_style))
    elements.append(Spacer(1, 1*cm))
    
    # Test 2: Heading with AMIRI_BOLD
    print("   Creating heading style with AMIRI_BOLD...")
    heading_style = ParagraphStyle(
        'ArabicHeading',
        parent=styles['Heading1'],
        alignment=TA_RIGHT,
        fontSize=14,
        textColor=colors.HexColor('#6d3a46'),
        spaceAfter=10,
        fontName=AMIRI_BOLD
    )
    
    heading_text = reshape_arabic("العنوان الرئيسي - اختبار خط Amiri Bold")
    elements.append(Paragraph(heading_text, heading_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Test 3: Body text with AMIRI_REGULAR
    print("   Creating body style with AMIRI_REGULAR...")
    body_style = ParagraphStyle(
        'ArabicBody',
        parent=styles['BodyText'],
        alignment=TA_RIGHT,
        fontSize=11,
        spaceAfter=10,
        fontName=AMIRI_REGULAR
    )
    
    body_text = reshape_arabic(
        "هذا نص تجريبي بالخط العربي Amiri Regular. "
        "يجب أن يظهر النص العربي بشكل واضح وصحيح، "
        "وليس كمربعات سوداء أو رموز غير مفهومة. "
        "إذا ظهر النص بشكل صحيح، فهذا يعني أن الخط العربي يعمل بشكل سليم."
    )
    elements.append(Paragraph(body_text, body_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Test 4: Table with Arabic text
    print("   Creating table with Arabic text...")
    table_data = [
        [reshape_arabic("المادة"), reshape_arabic("الإجمالي"), reshape_arabic("المُنجز"), reshape_arabic("النسبة")],
        [reshape_arabic("الرياضيات"), reshape_arabic("20"), reshape_arabic("18"), reshape_arabic("90%")],
        [reshape_arabic("اللغة العربية"), reshape_arabic("15"), reshape_arabic("12"), reshape_arabic("80%")],
        [reshape_arabic("العلوم"), reshape_arabic("18"), reshape_arabic("16"), reshape_arabic("88.9%")],
    ]
    
    table = Table(table_data, colWidths=[4*cm, 3*cm, 3*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6d3a46')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), AMIRI_BOLD),
        ('FONTNAME', (0, 1), (-1, -1), AMIRI_REGULAR),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Test 5: Numbers and special characters
    numbers_text = reshape_arabic("الأرقام العربية: ١٢٣٤٥٦٧٨٩٠ | الأرقام الإنجليزية: 0123456789")
    elements.append(Paragraph(numbers_text, body_style))
    
    # Build PDF
    print("   Building PDF document...")
    doc.build(elements)
    
    print(f"   ✓ PDF created successfully: {output_path}")
    print(f"   ✓ File size: {output_path.stat().st_size} bytes")
    
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 5: Summary
print("\n" + "=" * 60)
print("✅ TEST COMPLETED SUCCESSFULLY!")
print("=" * 60)
print(f"\n📄 Output file: {output_path}")
print("\nPlease open the PDF file and check:")
print("  1. Title should be in Arabic (bold)")
print("  2. Heading should be in Arabic (bold)")
print("  3. Body text should be in Arabic (regular)")
print("  4. Table should display Arabic text correctly")
print("  5. Numbers should display correctly")
print("\nIf you see black squares (▯▯▯) instead of Arabic text,")
print("the font is not being applied correctly.")
print("\n" + "=" * 60)

