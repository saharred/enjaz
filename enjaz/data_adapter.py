"""
Data adapter to convert LMS format to expected analysis format.
"""


def convert_lms_to_analysis_format(lms_data):
    """
    Convert data from LMS format to the format expected by analysis.py.
    
    Args:
        lms_data: List of sheet data from data_ingest_lms.py
    
    Returns:
        list: Data in the format expected by analysis.py
    """
    converted_data = []
    
    for sheet in lms_data:
        # Extract sheet info
        sheet_name = sheet['sheet_name']
        subject = sheet['subject']
        class_code = sheet['class_code']
        week_name = sheet.get('week_name', 'Week 1')
        
        # Convert students data
        for student in sheet['students']:
            converted_data.append({
                'sheet_name': sheet_name,
                'subject': subject,
                'class_code': class_code,
                'week_name': week_name,
                'student_name': student['student_name'],
                'total_due': student['total_due'],
                'completed': student['completed'],
                'not_submitted': student['not_submitted'],
                'completion_rate': student['completion_rate'],
                'has_due': student['has_due'],
                'assessments': student.get('assessments', [])
            })
    
    return converted_data

