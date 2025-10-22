"""
Horizontal Comprehensive Analysis Report Module
Creates detailed analytical reports with one row per student showing all subjects
"""

import pandas as pd
from typing import List, Dict
from enjaz.analysis import get_band, get_band_emoji
from enjaz.parent_recommendations import get_parent_recommendation


def create_horizontal_comprehensive_report(all_data: List[Dict]) -> pd.DataFrame:
    """
    Create comprehensive report with each row showing one student with all subjects:
    - Student name
    - Grade
    - Section
    - Subject 1 Total
    - Subject 1 Completed
    - Subject 2 Total
    - Subject 2 Completed
    - ... (for all subjects)
    - Overall completion rate
    - Band category
    - Recommendation
    
    Args:
        all_data: List of sheet data dictionaries
    
    Returns:
        DataFrame with horizontal comprehensive report
    """
    
    # Collect all student data
    student_data = {}
    all_subjects = set()
    
    for sheet_data in all_data:
        subject = sheet_data.get('subject', sheet_data.get('sheet_name', 'غير محدد'))
        all_subjects.add(subject)
        grade = sheet_data.get('grade', '')
        section = sheet_data.get('section', '')
        
        for student in sheet_data['students']:
            student_name = student['student_name']
            
            if student_name not in student_data:
                student_data[student_name] = {
                    'grade': grade,
                    'section': section,
                    'subjects': {}
                }
            
            # Add subject data
            if student['has_due']:
                student_data[student_name]['subjects'][subject] = {
                    'total_due': student['total_due'],
                    'completed': student['completed'],
                    'completion_rate': student['completion_rate']
                }
    
    # Sort subjects alphabetically
    sorted_subjects = sorted(list(all_subjects))
    
    # Create rows for each student
    report_rows = []
    
    for student_name, data in student_data.items():
        if not data['subjects']:
            continue
        
        # Calculate overall completion rate
        total_due_all = sum(s['total_due'] for s in data['subjects'].values())
        total_completed_all = sum(s['completed'] for s in data['subjects'].values())
        overall_rate = 100 * total_completed_all / total_due_all if total_due_all > 0 else 0
        
        # Get band and recommendation
        band = get_band(overall_rate)
        emoji = get_band_emoji(overall_rate)
        recommendation = get_parent_recommendation(overall_rate)
        
        # Create row
        row = {
            'اسم الطالب': student_name,
            'الصف': data['grade'],
            'الشعبة': data['section']
        }
        
        # Add columns for each subject (Total and Completed)
        for subject in sorted_subjects:
            if subject in data['subjects']:
                row[f'{subject} - إجمالي'] = data['subjects'][subject]['total_due']
                row[f'{subject} - منجز'] = data['subjects'][subject]['completed']
            else:
                row[f'{subject} - إجمالي'] = 0
                row[f'{subject} - منجز'] = 0
        
        # Add overall metrics
        row['نسبة الحل (%)'] = round(overall_rate, 1)
        row['الفئة'] = f"{emoji} {band}"
        row['التوصية'] = recommendation
        
        report_rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(report_rows)
    
    # Sort by student name
    if not df.empty:
        df = df.sort_values('اسم الطالب')
        df = df.reset_index(drop=True)
    
    return df

