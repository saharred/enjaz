"""
Teacher Report Module - Links teacher data with student grades
"""

import pandas as pd


def create_teacher_specific_report(all_data, teacher_subjects):
    """
    Create a report for a specific teacher by linking their subjects with student data.
    
    Args:
        all_data: List of all sheet data (student grades)
        teacher_subjects: DataFrame with teacher's subjects (from teachers file)
    
    Returns:
        dict: Teacher report data with statistics
    """
    # Initialize report data
    report_data = {
        'total_subjects': 0,
        'total_students': 0,
        'overall_completion_rate': 0.0,
        'details_df': None,
        'subjects_data': []
    }
    
    if teacher_subjects.empty or not all_data:
        return None
    
    # Get teacher's subjects and sections
    teacher_subject_list = []
    for _, row in teacher_subjects.iterrows():
        # Handle different column name variations
        subject = row.get('المادة', row.get('المادة الدراسية', row.get('subject', '')))
        section = row.get('الشعبة', row.get('section', ''))
        grade = row.get('الصف', row.get('grade', ''))
        
        teacher_subject_list.append({
            'subject': subject,
            'section': section,
            'grade': grade
        })
    
    # Match teacher's subjects with student data sheets
    matched_sheets = []
    total_completion = 0
    total_students_count = 0
    
    for sheet_data in all_data:
        sheet_subject = sheet_data.get('subject', '')
        sheet_section = sheet_data.get('section', '')
        sheet_grade = sheet_data.get('grade', '')
        
        # Check if this sheet matches any of teacher's subjects
        for teacher_subj in teacher_subject_list:
            # Match by subject and section
            subject_match = (teacher_subj['subject'].strip().lower() == sheet_subject.strip().lower())
            section_match = (str(teacher_subj['section']).strip() == str(sheet_section).strip())
            
            if subject_match and section_match:
                # Calculate statistics for this subject/section
                students = sheet_data.get('students', [])
                total_due = 0
                completed = 0
                
                for student in students:
                    if student.get('has_due', True):
                        total_due += student.get('total_due', 0)
                        completed += student.get('completed', 0)
                
                completion_rate = (completed / total_due * 100) if total_due > 0 else 0
                
                matched_sheets.append({
                    'المادة/الشعبة': f"{sheet_subject} - {sheet_section}",
                    'الصف': sheet_grade,
                    'عدد الطلاب': len(students),
                    'إجمالي التقييمات': total_due,
                    'المُنجز': completed,
                    'نسبة الإنجاز': round(completion_rate, 1)
                })
                
                total_completion += completion_rate
                total_students_count += len(students)
                break
    
    # If no matches found
    if not matched_sheets:
        return None
    
    # Calculate overall statistics
    report_data['total_subjects'] = len(matched_sheets)
    report_data['total_students'] = total_students_count
    report_data['overall_completion_rate'] = round(total_completion / len(matched_sheets), 1) if matched_sheets else 0
    report_data['details_df'] = pd.DataFrame(matched_sheets)
    report_data['subjects_data'] = matched_sheets
    
    return report_data


def aggregate_teacher_data(all_data, selected_indices):
    """
    Aggregate data from multiple selected sheets for teacher report.
    
    Args:
        all_data: List of all sheet data
        selected_indices: List of indices of selected sheets
    
    Returns:
        dict: Aggregated teacher data
    """
    # Import from enjaz module
    try:
        from enjaz.teacher_report import aggregate_teacher_data as enjaz_aggregate
        return enjaz_aggregate(all_data, selected_indices)
    except ImportError:
        # Fallback simple implementation
        teacher_data = {
            'sheets': [],
            'all_students': [],
            'total_students': 0,
            'total_assessments': 0,
            'total_completed': 0,
            'average_completion': 0.0
        }
        
        for idx in selected_indices:
            if idx < len(all_data):
                sheet_data = all_data[idx]
                teacher_data['sheets'].append({
                    'name': sheet_data.get('sheet_name', ''),
                    'subject': sheet_data.get('subject', ''),
                    'class_code': sheet_data.get('class_code', '')
                })
                
                for student in sheet_data.get('students', []):
                    teacher_data['total_assessments'] += student.get('total_due', 0)
                    teacher_data['total_completed'] += student.get('completed', 0)
                    teacher_data['all_students'].append(student)
        
        teacher_data['total_students'] = len(teacher_data['all_students'])
        if teacher_data['total_assessments'] > 0:
            teacher_data['average_completion'] = round(
                100 * teacher_data['total_completed'] / teacher_data['total_assessments'], 2
            )
        
        return teacher_data


def export_teacher_report_to_excel(teacher_data, output_path, teacher_name="المعلم/ة"):
    """
    Export teacher report to Excel file.
    
    Args:
        teacher_data: Aggregated teacher data
        output_path: Path to save Excel file
        teacher_name: Name of the teacher
    
    Returns:
        str: Path to saved file
    """
    # Import from enjaz module
    try:
        from enjaz.teacher_report import export_teacher_report_to_excel as enjaz_export
        return enjaz_export(teacher_data, output_path, teacher_name)
    except ImportError:
        # Fallback simple implementation
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Overview sheet
            overview_data = {
                'البيان': [
                    'اسم المعلم/ة',
                    'عدد المواد/الشعب',
                    'إجمالي الطلاب',
                    'متوسط الإنجاز'
                ],
                'القيمة': [
                    teacher_name,
                    len(teacher_data.get('sheets', [])),
                    teacher_data.get('total_students', 0),
                    f"{teacher_data.get('average_completion', 0):.1f}%"
                ]
            }
            overview_df = pd.DataFrame(overview_data)
            overview_df.to_excel(writer, sheet_name='نظرة عامة', index=False)
        
        return output_path

