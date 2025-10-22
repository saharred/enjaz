"""
School Report Module for Enjaz Application.
Generates comprehensive school-wide reports with horizontal layout showing all subjects for each student.
"""

import pandas as pd
from enjaz.analysis import get_band, get_band_emoji, BAND_LABELS


def create_horizontal_school_report(all_data):
    """
    Create a horizontal school report where each student has all their subjects in one row.
    
    Format: اسم الطالب | المستوى | الشعبة | المادة1 إجمالي | المادة1 منجز | المادة2 إجمالي | المادة2 منجز | ... | نسبة الحل العامة | الفئة
    
    Args:
        all_data: List of all sheet data
    
    Returns:
        pd.DataFrame: Horizontal school report
    """
    # First, collect all unique subjects
    all_subjects = []
    for sheet_data in all_data:
        subject = sheet_data.get('subject', sheet_data.get('sheet_name', ''))
        if subject not in all_subjects:
            all_subjects.append(subject)
    
    # Sort subjects alphabetically
    all_subjects.sort()
    
    # Collect student data
    student_records = {}
    
    for sheet_data in all_data:
        subject = sheet_data.get('subject', sheet_data.get('sheet_name', ''))
        
        for student in sheet_data['students']:
            if not student.get('has_due', True):
                continue
            
            student_name = student['student_name']
            
            # Initialize student record if not exists
            if student_name not in student_records:
                student_records[student_name] = {
                    'اسم الطالب': student_name,
                    'المستوى': sheet_data.get('grade', ''),
                    'الشعبة': sheet_data.get('section', ''),
                    'subjects': {},
                    'total_due': 0,
                    'total_completed': 0
                }
            
            # Add subject data
            student_records[student_name]['subjects'][subject] = {
                'total': student['total_due'],
                'completed': student['completed']
            }
            
            student_records[student_name]['total_due'] += student['total_due']
            student_records[student_name]['total_completed'] += student['completed']
    
    # Build rows for DataFrame
    rows = []
    
    for student_name, record in sorted(student_records.items()):
        row = {
            'اسم الطالب': student_name,
            'المستوى': record['المستوى'],
            'الشعبة': record['الشعبة']
        }
        
        # Add columns for each subject
        for subject in all_subjects:
            if subject in record['subjects']:
                row[f'{subject} - إجمالي'] = record['subjects'][subject]['total']
                row[f'{subject} - منجز'] = record['subjects'][subject]['completed']
            else:
                row[f'{subject} - إجمالي'] = 0
                row[f'{subject} - منجز'] = 0
        
        # Calculate overall completion rate
        if record['total_due'] > 0:
            overall_rate = round(100 * record['total_completed'] / record['total_due'], 2)
        else:
            overall_rate = 0.0
        
        band = get_band(overall_rate)
        emoji = get_band_emoji(band)
        
        row['نسبة الحل العامة'] = f"{overall_rate:.1f}%"
        row['الفئة'] = f"{emoji} {band}"
        
        rows.append(row)
    
    df = pd.DataFrame(rows)
    return df


def create_filtered_school_report(all_data, selected_grades=None, selected_sections=None):
    """
    Create a filtered school report based on selected grades and sections.
    
    Args:
        all_data: List of all sheet data
        selected_grades: List of selected grade levels (e.g., ['7', '8'])
        selected_sections: List of selected sections (e.g., ['1', '2'])
    
    Returns:
        pd.DataFrame: Filtered horizontal school report
    """
    # Filter data based on selections
    filtered_data = []
    
    for sheet_data in all_data:
        grade = sheet_data.get('grade', '')
        section = sheet_data.get('section', '')
        
        # Check if this sheet matches the filters
        grade_match = (selected_grades is None or 
                      len(selected_grades) == 0 or 
                      grade in selected_grades)
        
        section_match = (selected_sections is None or 
                        len(selected_sections) == 0 or 
                        section in selected_sections)
        
        if grade_match and section_match:
            filtered_data.append(sheet_data)
    
    if not filtered_data:
        return pd.DataFrame()
    
    return create_horizontal_school_report(filtered_data)


def export_school_report_to_excel(df, output_path, school_info=None):
    """
    Export school report to Excel with formatting and school information header.
    
    Args:
        df: School report DataFrame
        output_path: Path to save Excel file
        school_info: Dictionary containing school information
    
    Returns:
        str: Path to saved file
    """
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    from openpyxl.drawing.image import Image as XLImage
    from pathlib import Path
    from datetime import datetime
    
    if school_info is None:
        from enjaz.school_info import load_school_info
        school_info = load_school_info()
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Write data starting from row 10 to leave space for header
        df.to_excel(writer, sheet_name='تقرير المدرسة', index=False, startrow=9)
        
        # Get the worksheet
        worksheet = writer.sheets['تقرير المدرسة']
        
        # Add school header information
        header_font = Font(name='Arial', size=14, bold=True)
        normal_font = Font(name='Arial', size=11)
        center_alignment = Alignment(horizontal='center', vertical='center')
        right_alignment = Alignment(horizontal='right', vertical='center')
        
        # Add ministry logo if exists
        assets_path = Path(__file__).parent / 'assets'
        logo_path = assets_path / 'ministry_logo.png'
        if logo_path.exists():
            try:
                img = XLImage(str(logo_path))
                img.width = 80
                img.height = 80
                worksheet.add_image(img, 'A1')
            except:
                pass
        
        # School name
        worksheet['D1'] = school_info.get('school_name', '')
        worksheet['D1'].font = Font(name='Arial', size=16, bold=True)
        worksheet['D1'].alignment = center_alignment
        
        # Report title
        worksheet['D2'] = 'تقرير المدرسة الشامل'
        worksheet['D2'].font = Font(name='Arial', size=14, bold=True)
        worksheet['D2'].alignment = center_alignment
        
        # Date
        worksheet['D3'] = f"التاريخ: {datetime.now().strftime('%Y-%m-%d')}"
        worksheet['D3'].font = normal_font
        worksheet['D3'].alignment = center_alignment
        
        # School leadership information
        row = 5
        leadership = [
            ('مدير المدرسة', school_info.get('principal', '')),
            ('النائب الأكاديمي', school_info.get('academic_deputy', '')),
            ('النائب الإداري', school_info.get('admin_deputy', '')),
            ('منسق المشاريع', school_info.get('projects_coordinator', ''))
        ]
        
        for title, name in leadership:
            if name:
                worksheet[f'B{row}'] = f"{title}:"
                worksheet[f'B{row}'].font = Font(name='Arial', size=10, bold=True)
                worksheet[f'B{row}'].alignment = right_alignment
                
                worksheet[f'C{row}'] = name
                worksheet[f'C{row}'].font = Font(name='Arial', size=10)
                worksheet[f'C{row}'].alignment = right_alignment
                
                row += 1
        
        # Auto-adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
        
        # Format header row (row 10)
        header_fill = PatternFill(start_color='8A1538', end_color='8A1538', fill_type='solid')
        header_font_white = Font(name='Arial', size=11, bold=True, color='FFFFFF')
        
        for cell in worksheet[10]:
            cell.fill = header_fill
            cell.font = header_font_white
            cell.alignment = center_alignment
    
    return output_path


def get_unique_grades(all_data):
    """
    Get list of unique grade levels from data.
    
    Args:
        all_data: List of all sheet data
    
    Returns:
        list: Sorted list of unique grades
    """
    grades = set()
    for sheet_data in all_data:
        grade = sheet_data.get('grade', '')
        if grade:
            grades.add(grade)
    return sorted(list(grades))


def get_unique_sections(all_data):
    """
    Get list of unique sections from data.
    
    Args:
        all_data: List of all sheet data
    
    Returns:
        list: Sorted list of unique sections
    """
    sections = set()
    for sheet_data in all_data:
        section = sheet_data.get('section', '')
        if section:
            sections.add(section)
    return sorted(list(sections))


def create_descriptive_report(df):
    """
    Create a descriptive statistical report from the school data.
    
    Args:
        df: School report DataFrame
    
    Returns:
        str: Formatted descriptive report in Arabic
    """
    if df.empty:
        return "لا توجد بيانات لإنشاء التقرير الوصفي."
    
    total_students = len(df)
    
    # Count students by band
    band_counts = {}
    for band_label in BAND_LABELS:
        count = df['الفئة'].str.contains(band_label).sum()
        if count > 0:
            band_counts[band_label] = count
    
    # Extract completion rates
    completion_rates = df['نسبة الحل العامة'].str.rstrip('%').astype(float)
    avg_completion = completion_rates.mean()
    max_completion = completion_rates.max()
    min_completion = completion_rates.min()
    
    # Build descriptive report
    report = f"""
📊 التقرير الوصفي لأداء المدرسة
{'=' * 50}

إجمالي عدد الطلاب: {total_students} طالب/ة

متوسط نسبة الإنجاز العامة: {avg_completion:.1f}%
أعلى نسبة إنجاز: {max_completion:.1f}%
أدنى نسبة إنجاز: {min_completion:.1f}%

{'=' * 50}
توزيع الطلاب حسب الفئات:
{'=' * 50}

"""
    
    for band, count in band_counts.items():
        percentage = (count / total_students * 100)
        emoji = get_band_emoji(band)
        report += f"{emoji} {band}: {count} طالب/ة ({percentage:.1f}%)\n"
    
    report += f"\n{'=' * 50}\n"
    
    # Add recommendations based on overall performance
    if avg_completion >= 90:
        report += """
التوصيات:
✅ الأداء العام للمدرسة ممتاز جداً
• الاستمرار على هذا النهج المتميز
• توثيق أفضل الممارسات ومشاركتها
• تكريم الطلاب والمعلمين المتميزين
"""
    elif avg_completion >= 75:
        report += """
التوصيات:
🌟 الأداء العام للمدرسة جيد جداً
• العمل على الارتقاء إلى مستوى الامتياز
• تعزيز متابعة الطلاب الذين يحتاجون دعم
• تبادل الخبرات بين المعلمين
"""
    elif avg_completion >= 60:
        report += """
التوصيات:
👍 الأداء العام للمدرسة جيد
• تكثيف المتابعة والتذكير المستمر
• التواصل مع أولياء الأمور
• وضع خطط تحسين للطلاب الضعفاء
"""
    else:
        report += """
التوصيات:
⚠️ الأداء العام للمدرسة يحتاج إلى تحسين عاجل
• عقد اجتماعات طارئة مع المعلمين
• تكثيف التواصل مع أولياء الأمور
• وضع خطط علاجية فورية
• متابعة يومية للطلاب
"""
    
    report += f"\n{'=' * 50}\n"
    report += "تم إنشاء هذا التقرير بواسطة نظام إنجاز\n"
    report += "نظام تحليل التقييمات الإلكترونية الأسبوعية\n"
    
    return report

