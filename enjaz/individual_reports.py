"""
Individual Reports Module for Enjaz Application.
Generates professional PDF reports for students and classes.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, 
    Spacer, Image, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from io import BytesIO
import arabic_reshaper
from bidi.algorithm import get_display
import qrcode
from pathlib import Path

from enjaz.analysis import get_band, get_band_color
from enjaz.recommendations import get_recommendation_for_band
from enjaz.school_info import load_school_info, get_qr_links
from enjaz.pdf_fonts import get_arabic_font_name, AMIRI_REGULAR, AMIRI_BOLD


def reshape_arabic(text):
    """Reshape Arabic text for PDF display."""
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)


def create_qr_code(data, size=2*cm):
    """
    Create QR code image.
    
    Args:
        data: URL or text to encode
        size: Size of QR code
    
    Returns:
        Image: ReportLab Image object
    """
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to buffer
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return Image(buffer, width=size, height=size)


def create_student_individual_report(student_name, all_data, class_name, section):
    """
    Create comprehensive individual report for a student.
    
    Args:
        student_name: Student name
        all_data: List of sheet data
        class_name: Class/grade name
        section: Section/division
    
    Returns:
        BytesIO: PDF file buffer
    """
    buffer = BytesIO()
    school_info = load_school_info()
    qr_links = get_qr_links()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=1.5*cm,
        bottomMargin=2*cm
    )
    
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'ArabicTitle',
        parent=styles['Title'],
        alignment=TA_CENTER,
        fontSize=16,
        textColor=colors.HexColor('#6d3a46'),
        spaceAfter=10,
        fontName=AMIRI_BOLD
    )
    
    heading_style = ParagraphStyle(
        'ArabicHeading',
        parent=styles['Heading2'],
        alignment=TA_RIGHT,
        fontSize=12,
        textColor=colors.HexColor('#6d3a46'),
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'ArabicBody',
        parent=styles['BodyText'],
        alignment=TA_RIGHT,
        fontSize=10,
        spaceAfter=6
    )
    
    # === HEADER WITH LOGOS ===
    assets_path = Path(__file__).parent / 'assets'
    
    # Header table with logos
    header_data = []
    
    # Row 1: MOE Logo + Title + School Logo (if exists)
    row1 = []
    
    # MOE Logo (left in RTL = right visually)
    moe_logo_path = assets_path / 'moe_logo.png'
    if moe_logo_path.exists():
        moe_logo = Image(str(moe_logo_path), width=4*cm, height=1.1*cm)
        row1.append(moe_logo)
    else:
        row1.append('')
    
    # Title
    title_text = reshape_arabic("تقرير أداء الطالب نظام قطر للتعليم")
    row1.append(Paragraph(title_text, title_style))
    
    # Enjaz Logo (right in RTL = left visually)
    enjaz_logo_path = assets_path / 'logo.png'
    if enjaz_logo_path.exists():
        enjaz_logo = Image(str(enjaz_logo_path), width=2*cm, height=2*cm)
        row1.append(enjaz_logo)
    else:
        row1.append('')
    
    header_data.append(row1)
    
    # Create header table
    header_table = Table(header_data, colWidths=[5*cm, 7*cm, 3*cm])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(header_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # === STUDENT INFO ===
    info_title = reshape_arabic("معلومات الطالب")
    elements.append(Paragraph(info_title, heading_style))
    
    info_data = [
        [reshape_arabic("الشعبة:"), reshape_arabic(section), reshape_arabic("الصف:"), reshape_arabic(class_name)],
        [reshape_arabic("اسم الطالب:"), reshape_arabic(student_name), '', '']
    ]
    
    info_table = Table(info_data, colWidths=[3*cm, 5*cm, 2*cm, 5*cm])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # === SUBJECT-WISE TABLE ===
    table_data = []
    
    # Headers
    headers = [
        reshape_arabic("عدد التقييمات المتبقية"),
        reshape_arabic("عدد التقييمات المُنجزة"),
        reshape_arabic("عدد التقييمات الإجمالي"),
        reshape_arabic("المادة")
    ]
    table_data.append(headers)
    
    # Collect student data from all subjects
    total_due = 0
    total_completed = 0
    
    for sheet_data in all_data:
        subject = sheet_data.get('subject', sheet_data['sheet_name'])
        
        # Find student in this sheet
        for student in sheet_data['students']:
            if student['student_name'] == student_name:
                due = student['total_due']
                completed = student['completed']
                remaining = due - completed
                
                total_due += due
                total_completed += completed
                
                row = [
                    reshape_arabic(str(remaining)),
                    reshape_arabic(str(completed)),
                    reshape_arabic(str(due)),
                    reshape_arabic(subject)
                ]
                table_data.append(row)
                break
    
    # Create table
    subject_table = Table(table_data, colWidths=[4*cm, 4*cm, 4*cm, 3*cm])
    subject_table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6d3a46')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        
        # Data rows
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ]))
    
    elements.append(subject_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # === STATISTICS ===
    stats_title = reshape_arabic("الإحصائيات:")
    elements.append(Paragraph(stats_title, heading_style))
    
    completion_rate = round(100 * total_completed / total_due, 1) if total_due > 0 else 0
    remaining = total_due - total_completed
    
    stats_data = [
        [reshape_arabic("نسبة حل التقييمات"), reshape_arabic("متبقي"), reshape_arabic("منجز")],
        [reshape_arabic(f"{completion_rate}%"), reshape_arabic(str(remaining)), reshape_arabic(str(total_completed))]
    ]
    
    stats_table = Table(stats_data, colWidths=[5*cm, 5*cm, 5*cm])
    stats_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F0F0F0')),
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # === RECOMMENDATION ===
    rec_title = reshape_arabic("توصية منسق المشاريع:")
    elements.append(Paragraph(rec_title, heading_style))
    
    band = get_band(completion_rate)
    recommendation = get_recommendation_for_band(band, level='student')
    rec_text = reshape_arabic(recommendation)
    elements.append(Paragraph(rec_text, body_style))
    
    elements.append(Spacer(1, 0.5*cm))
    
    # === QR CODES ===
    qr_title = reshape_arabic("روابط مهمة:")
    elements.append(Paragraph(qr_title, heading_style))
    
    qr_data = []
    qr_row = []
    
    # QR 1: LMS Link
    qr1 = create_qr_code(qr_links['lms_link'], size=2.5*cm)
    qr1_label = reshape_arabic("رابط نظام قطر:")
    qr_row.append([qr1, Paragraph(qr1_label, body_style)])
    
    # QR 2: Password Recovery
    qr2 = create_qr_code(qr_links['password_recovery'], size=2.5*cm)
    qr2_label = reshape_arabic("موقع استعادة كلمة المرور:")
    qr_row.append([qr2, Paragraph(qr2_label, body_style)])
    
    # QR 3: Qatar TV
    qr3 = create_qr_code(qr_links['qatar_tv'], size=2.5*cm)
    qr3_label = reshape_arabic("قناة قطر للتعليم على نظام قطر للتعليم:")
    qr_row.append([qr3, Paragraph(qr3_label, body_style)])
    
    qr_data.append(qr_row)
    
    qr_table = Table(qr_data, colWidths=[5*cm, 5*cm, 5*cm])
    qr_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(qr_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # === FOOTER WITH STAFF INFO ===
    footer_data = [
        [reshape_arabic(f"منسق المشاريع/ {school_info['projects_coordinator']}")],
        [reshape_arabic(f"النائب الأكاديمي/ {school_info['academic_deputy']}"), 
         reshape_arabic(f"النائب الإداري/ {school_info['admin_deputy']}")],
        [reshape_arabic(f"مدير المدرسة/ {school_info['principal']}")],
        [reshape_arabic(school_info['vision'])]
    ]
    
    footer_table = Table(footer_data, colWidths=[15*cm])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    elements.append(footer_table)
    
    # Build PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer


def create_class_subject_report(subject, class_code, sheet_data):
    """
    Create individual report for a class/subject combination.
    
    Args:
        subject: Subject name
        class_code: Class code
        sheet_data: Sheet data for this class/subject
    
    Returns:
        BytesIO: PDF file buffer
    """
    buffer = BytesIO()
    school_info = load_school_info()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=1.5*cm,
        bottomMargin=2*cm
    )
    
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'ArabicTitle',
        parent=styles['Title'],
        alignment=TA_CENTER,
        fontSize=16,
        textColor=colors.HexColor('#6d3a46'),
        spaceAfter=10
    )
    
    heading_style = ParagraphStyle(
        'ArabicHeading',
        parent=styles['Heading2'],
        alignment=TA_RIGHT,
        fontSize=12,
        textColor=colors.HexColor('#6d3a46'),
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'ArabicBody',
        parent=styles['BodyText'],
        alignment=TA_RIGHT,
        fontSize=10,
        spaceAfter=6
    )
    
    # === HEADER ===
    assets_path = Path(__file__).parent / 'assets'
    
    header_data = []
    row1 = []
    
    # MOE Logo
    moe_logo_path = assets_path / 'moe_logo.png'
    if moe_logo_path.exists():
        moe_logo = Image(str(moe_logo_path), width=4*cm, height=1.1*cm)
        row1.append(moe_logo)
    else:
        row1.append('')
    
    # Title
    title_text = reshape_arabic(f"تقرير المادة والشعبة - {subject} {class_code}")
    row1.append(Paragraph(title_text, title_style))
    
    # Enjaz Logo
    enjaz_logo_path = assets_path / 'logo.png'
    if enjaz_logo_path.exists():
        enjaz_logo = Image(str(enjaz_logo_path), width=2*cm, height=2*cm)
        row1.append(enjaz_logo)
    else:
        row1.append('')
    
    header_data.append(row1)
    
    header_table = Table(header_data, colWidths=[5*cm, 7*cm, 3*cm])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(header_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # === STUDENT LIST TABLE ===
    table_data = []
    
    # Headers
    headers = [
        reshape_arabic("نسبة الإنجاز"),
        reshape_arabic("المتبقي"),
        reshape_arabic("المُنجز"),
        reshape_arabic("الإجمالي"),
        reshape_arabic("اسم الطالب")
    ]
    table_data.append(headers)
    
    # Student rows
    for student in sheet_data['students']:
        if not student['has_due']:
            continue
        
        completion = student['completion_rate']
        row = [
            reshape_arabic(f"{completion:.1f}%"),
            reshape_arabic(str(student['not_submitted'])),
            reshape_arabic(str(student['completed'])),
            reshape_arabic(str(student['total_due'])),
            reshape_arabic(student['student_name'])
        ]
        table_data.append(row)
    
    # Create table
    student_table = Table(table_data, colWidths=[3*cm, 2.5*cm, 2.5*cm, 2.5*cm, 4.5*cm])
    student_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6d3a46')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        
        # Data
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ]))
    
    elements.append(student_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # === CLASS STATISTICS ===
    students_with_due = [s for s in sheet_data['students'] if s['has_due']]
    
    if students_with_due:
        avg_completion = sum(s['completion_rate'] for s in students_with_due) / len(students_with_due)
        total_students = len(students_with_due)
        
        stats_title = reshape_arabic("إحصائيات الصف:")
        elements.append(Paragraph(stats_title, heading_style))
        
        stats_text = reshape_arabic(
            f"عدد الطلاب: {total_students} | "
            f"متوسط نسبة الإنجاز: {avg_completion:.1f}%"
        )
        elements.append(Paragraph(stats_text, body_style))
        
        elements.append(Spacer(1, 0.5*cm))
        
        # === RECOMMENDATION ===
        rec_title = reshape_arabic("التوصيات:")
        elements.append(Paragraph(rec_title, heading_style))
        
        band = get_band(avg_completion)
        recommendation = get_recommendation_for_band(band, level='class')
        rec_text = reshape_arabic(recommendation)
        elements.append(Paragraph(rec_text, body_style))
    
    elements.append(Spacer(1, 0.5*cm))
    
    # === FOOTER ===
    footer_data = [
        [reshape_arabic(f"منسق المشاريع/ {school_info['projects_coordinator']}")],
        [reshape_arabic(f"النائب الأكاديمي/ {school_info['academic_deputy']}"), 
         reshape_arabic(f"النائب الإداري/ {school_info['admin_deputy']}")],
        [reshape_arabic(f"مدير المدرسة/ {school_info['principal']}")],
        [reshape_arabic(school_info['vision'])]
    ]
    
    footer_table = Table(footer_data, colWidths=[15*cm])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    
    elements.append(footer_table)
    
    # Build PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer

