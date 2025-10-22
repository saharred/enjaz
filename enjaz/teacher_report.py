"""
Teacher Report Module for Enjaz Application.
Generates comprehensive reports for teachers with multiple subjects/classes.
"""

import pandas as pd
from enjaz.analysis import get_band, get_band_emoji, BAND_LABELS
from enjaz.recommendations import get_class_recommendation_by_percentage


def aggregate_teacher_data(all_data, selected_sheet_indices):
    """
    Aggregate data from multiple selected sheets for teacher report.
    
    Args:
        all_data: List of all sheet data
        selected_sheet_indices: List of indices of selected sheets
    
    Returns:
        dict: Aggregated teacher data with statistics
    """
    teacher_data = {
        'sheets': [],
        'all_students': [],
        'total_students': 0,
        'total_assessments': 0,
        'total_completed': 0,
        'average_completion': 0.0,
        'band_distribution': {band: [] for band in BAND_LABELS},
        'students_by_band': {band: [] for band in BAND_LABELS}
    }
    
    student_names_seen = set()
    
    for idx in selected_sheet_indices:
        sheet_data = all_data[idx]
        teacher_data['sheets'].append({
            'name': sheet_data.get('sheet_name', ''),
            'subject': sheet_data.get('subject', ''),
            'class_code': sheet_data.get('class_code', ''),
            'grade': sheet_data.get('grade', ''),
            'section': sheet_data.get('section', '')
        })
        
        for student in sheet_data['students']:
            if not student.get('has_due', True):
                continue
            
            completion_rate = student['completion_rate']
            band = get_band(completion_rate)
            
            student_record = {
                'student_name': student['student_name'],
                'subject': sheet_data.get('subject', ''),
                'class_code': sheet_data.get('class_code', ''),
                'grade': sheet_data.get('grade', ''),
                'section': sheet_data.get('section', ''),
                'total_due': student['total_due'],
                'completed': student['completed'],
                'not_submitted': student['not_submitted'],
                'completion_rate': completion_rate,
                'band': band
            }
            
            teacher_data['all_students'].append(student_record)
            teacher_data['band_distribution'][band].append(student_record)
            
            # Track unique students
            if student['student_name'] not in student_names_seen:
                student_names_seen.add(student['student_name'])
                teacher_data['students_by_band'][band].append(student['student_name'])
            
            teacher_data['total_assessments'] += student['total_due']
            teacher_data['total_completed'] += student['completed']
    
    teacher_data['total_students'] = len(student_names_seen)
    
    if teacher_data['total_assessments'] > 0:
        teacher_data['average_completion'] = round(
            100 * teacher_data['total_completed'] / teacher_data['total_assessments'], 2
        )
    
    return teacher_data


def create_teacher_report_dataframe(teacher_data):
    """
    Create a comprehensive DataFrame for teacher report.
    
    Args:
        teacher_data: Aggregated teacher data
    
    Returns:
        pd.DataFrame: Teacher report data
    """
    rows = []
    
    for student in teacher_data['all_students']:
        emoji = get_band_emoji(student['band'])
        rows.append({
            'اسم الطالب': student['student_name'],
            'الصف': student.get('grade', ''),
            'الشعبة': student.get('section', ''),
            'المادة': student['subject'],
            'إجمالي التقييمات': student['total_due'],
            'المُنجز': student['completed'],
            'المتبقي': student['not_submitted'],
            'نسبة الإنجاز': f"{student['completion_rate']:.1f}%",
            'الفئة': f"{emoji} {student['band']}"
        })
    
    df = pd.DataFrame(rows)
    return df


def create_students_by_band_report(teacher_data):
    """
    Create a report showing student names grouped by performance band.
    
    Args:
        teacher_data: Aggregated teacher data
    
    Returns:
        dict: Student names organized by band
    """
    report = {}
    
    for band in BAND_LABELS:
        students = teacher_data['students_by_band'].get(band, [])
        if students:
            emoji = get_band_emoji(band)
            report[f"{emoji} {band}"] = {
                'count': len(students),
                'students': sorted(students)
            }
    
    return report


def format_teacher_report_for_email(teacher_data, teacher_name="المعلم/ة"):
    """
    Format teacher report as text suitable for email.
    
    Args:
        teacher_data: Aggregated teacher data
        teacher_name: Name of the teacher
    
    Returns:
        str: Formatted email text
    """
    email_text = f"""
تقرير إنجاز التقييمات الأسبوعية
{'=' * 50}

المعلم/ة: {teacher_name}
عدد المواد/الشعب: {len(teacher_data['sheets'])}
إجمالي الطلاب: {teacher_data['total_students']}
متوسط الإنجاز: {teacher_data['average_completion']:.1f}%

المواد والشعب المشمولة:
"""
    
    for sheet in teacher_data['sheets']:
        email_text += f"  • {sheet['subject']} - {sheet['class_code']}\n"
    
    email_text += f"\n{'=' * 50}\n"
    email_text += "توزيع الطلاب حسب الفئات:\n"
    email_text += f"{'=' * 50}\n\n"
    
    students_by_band = create_students_by_band_report(teacher_data)
    
    for band_label, data in students_by_band.items():
        email_text += f"\n{band_label} ({data['count']} طالب/ة):\n"
        email_text += "-" * 40 + "\n"
        for i, student in enumerate(data['students'], 1):
            email_text += f"{i}. {student}\n"
    
    email_text += f"\n{'=' * 50}\n"
    email_text += "التوصيات:\n"
    email_text += f"{'=' * 50}\n\n"
    
    recommendation = get_class_recommendation_by_percentage(
        teacher_data['average_completion'],
        "المواد المختارة"
    )
    email_text += recommendation
    
    email_text += f"\n\n{'=' * 50}\n"
    email_text += "تم إنشاء هذا التقرير بواسطة نظام إنجاز\n"
    email_text += "نظام تحليل التقييمات الإلكترونية الأسبوعية\n"
    
    return email_text


def create_band_summary_table(teacher_data):
    """
    Create a summary table showing count and percentage for each band.
    
    Args:
        teacher_data: Aggregated teacher data
    
    Returns:
        pd.DataFrame: Band summary table
    """
    rows = []
    total_records = len(teacher_data['all_students'])
    
    for band in BAND_LABELS:
        count = len(teacher_data['band_distribution'].get(band, []))
        percentage = (count / total_records * 100) if total_records > 0 else 0
        emoji = get_band_emoji(band)
        
        rows.append({
            'الفئة': f"{emoji} {band}",
            'عدد الطلاب': count,
            'النسبة': f"{percentage:.1f}%"
        })
    
    df = pd.DataFrame(rows)
    return df


def export_teacher_report_to_excel(teacher_data, output_path, teacher_name="المعلم/ة"):
    """
    Export teacher report to Excel file with multiple sheets.
    
    Args:
        teacher_data: Aggregated teacher data
        output_path: Path to save Excel file
        teacher_name: Name of the teacher
    
    Returns:
        str: Path to saved file
    """
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Sheet 1: Overview
        overview_data = {
            'البيان': [
                'اسم المعلم/ة',
                'عدد المواد/الشعب',
                'إجمالي الطلاب',
                'إجمالي التقييمات',
                'المُنجز',
                'متوسط الإنجاز'
            ],
            'القيمة': [
                teacher_name,
                len(teacher_data['sheets']),
                teacher_data['total_students'],
                teacher_data['total_assessments'],
                teacher_data['total_completed'],
                f"{teacher_data['average_completion']:.1f}%"
            ]
        }
        overview_df = pd.DataFrame(overview_data)
        overview_df.to_excel(writer, sheet_name='نظرة عامة', index=False)
        
        # Sheet 2: Detailed student data
        detailed_df = create_teacher_report_dataframe(teacher_data)
        detailed_df.to_excel(writer, sheet_name='تفاصيل الطلاب', index=False)
        
        # Sheet 3: Band summary
        band_summary_df = create_band_summary_table(teacher_data)
        band_summary_df.to_excel(writer, sheet_name='ملخص الفئات', index=False)
        
        # Sheet 4-9: Students by band
        for band in BAND_LABELS:
            students = teacher_data['students_by_band'].get(band, [])
            if students:
                band_df = pd.DataFrame({
                    'اسم الطالب': sorted(students)
                })
                # Clean sheet name (Excel has 31 char limit and special char restrictions)
                sheet_name = band[:20]  # Truncate if too long
                band_df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    return output_path

