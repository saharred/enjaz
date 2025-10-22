"""
Student profile PDF export module.
Generates Arabic RTL PDF reports for individual students.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from io import BytesIO
import arabic_reshaper
from bidi.algorithm import get_display

from enjaz.analysis import get_band, get_band_color


def reshape_arabic(text):
    """Reshape Arabic text for PDF display."""
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)


def create_student_profile_pdf(student_name, student_data, overall_band):
    """
    Create PDF report for individual student.
    
    Args:
        student_name: Student name
        student_data: List of dicts with subject-level data
        overall_band: Overall performance band
    
    Returns:
        BytesIO: PDF file buffer
    """
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Arabic RTL styles
    title_style = ParagraphStyle(
        'ArabicTitle',
        parent=styles['Title'],
        alignment=TA_CENTER,
        fontSize=18,
        textColor=colors.HexColor('#8A1538'),  # Qatar Maroon
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'ArabicHeading',
        parent=styles['Heading1'],
        alignment=TA_RIGHT,
        fontSize=14,
        textColor=colors.HexColor('#8A1538'),
        spaceAfter=10
    )
    
    body_style = ParagraphStyle(
        'ArabicBody',
        parent=styles['BodyText'],
        alignment=TA_RIGHT,
        fontSize=11,
        spaceAfter=10
    )
    
    # Header
    title_text = reshape_arabic(f"نظام تحليل التقييمات الإلكترونية الأسبوعية على قطر للتعليم")
    elements.append(Paragraph(title_text, title_style))
    
    subtitle_text = reshape_arabic(f"ملف الطالب: {student_name}")
    elements.append(Paragraph(subtitle_text, heading_style))
    
    elements.append(Spacer(1, 0.5*cm))
    
    # Overall band
    band_text = reshape_arabic(f"التقييم الإجمالي: {overall_band}")
    elements.append(Paragraph(band_text, heading_style))
    
    elements.append(Spacer(1, 0.5*cm))
    
    # Subject-level table
    table_title = reshape_arabic("الأداء حسب المادة")
    elements.append(Paragraph(table_title, heading_style))
    
    # Build table data
    table_data = []
    
    # Headers (RTL order: right to left)
    headers = [
        reshape_arabic("الفئة"),
        reshape_arabic("نسبة الإنجاز"),
        reshape_arabic("المكتمل"),
        reshape_arabic("المستحق"),
        reshape_arabic("المادة")
    ]
    table_data.append(headers)
    
    # Data rows
    for subject_info in student_data:
        row = [
            reshape_arabic(subject_info.get('band', 'N/A')),
            reshape_arabic(f"{subject_info.get('completion_rate', 0):.1f}%"),
            reshape_arabic(str(subject_info.get('completed', 0))),
            reshape_arabic(str(subject_info.get('total_due', 0))),
            reshape_arabic(subject_info.get('subject', ''))
        ]
        table_data.append(row)
    
    # Create table
    table = Table(table_data, colWidths=[3.5*cm, 3*cm, 2.5*cm, 2.5*cm, 4*cm])
    
    # Table style
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8A1538')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Data rows
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ]))
    
    elements.append(table)
    
    elements.append(Spacer(1, 1*cm))
    
    # Fixed advisory lines
    advisory_title = reshape_arabic("التوصيات:")
    elements.append(Paragraph(advisory_title, heading_style))
    
    advisory_text = reshape_arabic(
        "• تذكير الطلاب دائماً بحل التقييمات بنهاية كل حصة\n"
        "• رقمنة استراتيجية الصفوف المقلوبة بتوظيف نظام قطر للتعليم\n"
        "• التواصل مع أولياء الأمور لمتابعة تقدم الطالب"
    )
    elements.append(Paragraph(advisory_text, body_style))
    
    elements.append(Spacer(1, 1*cm))
    
    # Footer
    footer_text = reshape_arabic("مدرسة عثمان بن عفان النموذجية للبنين")
    elements.append(Paragraph(footer_text, heading_style))
    
    email_text = "Sahar.Osman@education.qa"
    elements.append(Paragraph(email_text, body_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF bytes
    buffer.seek(0)
    return buffer


def export_student_profile_pdf(student_name, all_data, overall_stats):
    """
    Export student profile to PDF.
    
    Args:
        student_name: Student name
        all_data: List of sheet data
        overall_stats: Overall statistics for student
    
    Returns:
        BytesIO: PDF file buffer
    """
    # Collect subject-level data
    student_data = []
    
    for sheet_data in all_data:
        subject = sheet_data.get('subject', sheet_data['sheet_name'])
        
        # Find student in this sheet
        for student in sheet_data['students']:
            if student['student_name'] == student_name:
                band = get_band(student['completion_rate'])
                
                student_data.append({
                    'subject': subject,
                    'total_due': student['total_due'],
                    'completed': student['completed'],
                    'completion_rate': student['completion_rate'],
                    'band': band
                })
                break
    
    # Get overall band
    overall_band = get_band(overall_stats.get('overall_completion_rate', 0))
    
    # Create PDF
    return create_student_profile_pdf(student_name, student_data, overall_band)

