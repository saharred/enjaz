"""
Reports module for Enjaz application.
Handles Excel and PDF export with Arabic branding.
"""

import pandas as pd
from io import BytesIO
import xlsxwriter
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
import arabic_reshaper
from bidi.algorithm import get_display


def reshape_arabic_text(text):
    """
    Reshape Arabic text for proper display in PDFs.
    
    Args:
        text: Arabic text string
    
    Returns:
        str: Reshaped text
    """
    if text is None or str(text).strip() == '':
        return ''
    
    reshaped_text = arabic_reshaper.reshape(str(text))
    bidi_text = get_display(reshaped_text)
    return bidi_text


def export_to_excel(dataframe, filename="report.xlsx"):
    """
    Export DataFrame to Excel with Arabic formatting.
    
    Args:
        dataframe: pandas DataFrame
        filename: Output filename
    
    Returns:
        BytesIO: Excel file buffer
    """
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        dataframe.to_excel(writer, index=False, sheet_name='التقرير')
        
        workbook = writer.book
        worksheet = writer.sheets['التقرير']
        
        # Add formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#8A1538',
            'font_color': 'white',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })
        
        # Write headers with formatting
        for col_num, value in enumerate(dataframe.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Set column widths
        for i, col in enumerate(dataframe.columns):
            max_len = max(
                dataframe[col].astype(str).apply(len).max(),
                len(str(col))
            ) + 2
            worksheet.set_column(i, i, max_len)
    
    output.seek(0)
    return output


def create_pdf_report(title, content_data, filename="report.pdf"):
    """
    Create a PDF report with Arabic branding.
    
    Args:
        title: Report title
        content_data: List of dictionaries with report content
        filename: Output filename
    
    Returns:
        BytesIO: PDF file buffer
    """
    output = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=3*cm,
        bottomMargin=3*cm
    )
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Arabic title style
    title_style = ParagraphStyle(
        'ArabicTitle',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        fontSize=18,
        textColor=colors.HexColor('#8A1538'),
        spaceAfter=20
    )
    
    # Arabic body style
    body_style = ParagraphStyle(
        'ArabicBody',
        parent=styles['Normal'],
        alignment=TA_RIGHT,
        fontSize=12,
        spaceAfter=10
    )
    
    # Add title
    title_text = reshape_arabic_text(title)
    elements.append(Paragraph(title_text, title_style))
    elements.append(Spacer(1, 1*cm))
    
    # Add content
    for item in content_data:
        if item['type'] == 'heading':
            heading_text = reshape_arabic_text(item['text'])
            elements.append(Paragraph(heading_text, title_style))
            elements.append(Spacer(1, 0.5*cm))
        
        elif item['type'] == 'paragraph':
            para_text = reshape_arabic_text(item['text'])
            elements.append(Paragraph(para_text, body_style))
        
        elif item['type'] == 'table':
            # Create table data with reshaped Arabic text
            table_data = []
            for row in item['data']:
                reshaped_row = [reshape_arabic_text(cell) for cell in row]
                table_data.append(reshaped_row)
            
            # Create table
            t = Table(table_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8A1538')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(t)
            elements.append(Spacer(1, 0.5*cm))
        
        elif item['type'] == 'spacer':
            elements.append(Spacer(1, 1*cm))
    
    # Add footer
    footer_text = reshape_arabic_text(
        "© 2025 — جميع الحقوق محفوظة | مدرسة عثمان بن عفّان النموذجية للبنين"
    )
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph(footer_text, body_style))
    
    # Build PDF
    doc.build(elements)
    
    output.seek(0)
    return output


def create_class_report_excel(sheet_data, class_stats):
    """
    Create Excel report for a specific class/subject.
    
    Args:
        sheet_data: Sheet data dictionary
        class_stats: Class statistics dictionary
    
    Returns:
        BytesIO: Excel file buffer
    """
    from .analysis import create_dataframe_for_class
    
    df = create_dataframe_for_class(sheet_data)
    return export_to_excel(df, filename=f"{sheet_data['sheet_name']}_report.xlsx")


def create_overall_report_excel(all_data, student_stats):
    """
    Create overall Excel report with all students and subjects.
    
    Args:
        all_data: All sheet data
        student_stats: Student statistics dictionary
    
    Returns:
        BytesIO: Excel file buffer
    """
    rows = []
    
    for name, stats in student_stats.items():
        rows.append({
            'اسم الطالب': name,
            'إجمالي المكتمل': stats['total_completed'],
            'إجمالي المطلوب': stats['total_assigned'],
            'النسبة المئوية': f"{stats['overall_completion_rate']:.1f}%" if stats['overall_completion_rate'] is not None else "N/A",
            'التصنيف الإجمالي': stats['overall_band']
        })
    
    df = pd.DataFrame(rows)
    df = df.sort_values('النسبة المئوية', ascending=False)
    
    return export_to_excel(df, filename="overall_report.xlsx")

