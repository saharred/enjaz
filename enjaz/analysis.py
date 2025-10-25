"""
Analysis module for Enjaz application.
Handles data analysis, banding, and statistics.

Version: 2.1 - Fixed band distribution calculation (2025-10-24)
"""

import pandas as pd
import numpy as np


# Band labels (must match these exactly)
BAND_LABELS = [
    "البلاتينية",
    "الذهبية",
    "الفضية",
    "البرونزية",
    "يحتاج إلى تطوير",
    "لا يستفيد من النظام"
]


def get_band(completion_rate):
    """
    Classify completion rate into performance bands.
    
    التصنيفات:
    - 💎 البلاتينية (Platinum): >= 90%
    - 🥇 الذهبية (Gold): >= 80%
    - 🥈 الفضية (Silver): >= 70%
    - 🥉 البرونزية (Bronze): >= 50%
    - ⚠️ يحتاج إلى تطوير: >= 1%
    - ❌ لا يستفيد من النظام: = 0%
    
    Args:
        completion_rate: Completion percentage (0-100) or None
    
    Returns:
        str: Band name in Arabic
    """
    if completion_rate is None:
        return "N/A"
    
    if completion_rate >= 90:
        return "البلاتينية"
    elif completion_rate >= 80:
        return "الذهبية"
    elif completion_rate >= 70:
        return "الفضية"
    elif completion_rate >= 50:
        return "البرونزية"
    elif completion_rate >= 1:
        return "يحتاج إلى تطوير"
    else:
        return "لا يستفيد من النظام"


def get_band_color(band):
    """
    Get color for each band.
    
    Args:
        band: Band name
    
    Returns:
        str: Hex color code
    """
    colors = {
        "البلاتينية": "#E5E4E2",      # Platinum
        "الذهبية": "#FFD700",        # Gold
        "الفضية": "#C0C0C0",        # Silver
        "البرونزية": "#CD7F32",    # Bronze
        "يحتاج إلى تطوير": "#FF6600", # Orange
        "لا يستفيد من النظام": "#C00000",  # Red
        "N/A": "#CCCCCC"
    }
    return colors.get(band, "#000000")


def get_band_emoji(band):
    """
    Get emoji for each band.
    
    Args:
        band: Band name
    
    Returns:
        str: Emoji
    """
    emojis = {
        "البلاتينية": "✅",
        "الذهبية": "🥇",
        "الفضية": "🥈",
        "البرونزية": "🥉",
        "يحتاج إلى تطوير": "⚠️",
        "لا يستفيد من النظام": "❌",
        "N/A": "➡️"
    }
    return emojis.get(band, "")


def calculate_student_overall_stats(all_data):
    """
    Calculate overall statistics for each student across all subjects.
    Only includes students with has_due=True.
    
    Args:
        all_data: List of sheet data from data_ingest
    
    Returns:
        dict: Student name -> overall stats
    """
    student_stats = {}
    
    for sheet_data in all_data:
        for student in sheet_data['students']:
            name = student['student_name']
            
            # Skip students without due assessments
            if not student.get('has_due', True):
                continue
            
            if name not in student_stats:
                student_stats[name] = {
                    'total_due': 0,
                    'total_completed': 0,
                    'subjects': []
                }
            
            student_stats[name]['total_due'] += student['total_due']
            student_stats[name]['total_completed'] += student['completed']
            student_stats[name]['subjects'].append({
                'subject': sheet_data['sheet_name'],
                'completion_rate': student['completion_rate'],
                'band': get_band(student['completion_rate'])
            })
    
    # Calculate overall completion rate and band
    for name, stats in student_stats.items():
        if stats['total_due'] > 0:
            stats['overall_completion_rate'] = round(100 * stats['total_completed'] / stats['total_due'], 2)
            stats['overall_band'] = get_band(stats['overall_completion_rate'])
        else:
            stats['overall_completion_rate'] = 0.0
            stats['overall_band'] = "N/A"
    
    return student_stats


def calculate_class_stats(sheet_data):
    """
    Calculate statistics for a class/subject.
    Only includes students with has_due=True.
    
    Args:
        sheet_data: Single sheet data dictionary
    
    Returns:
        dict: Class statistics
    """
    students = sheet_data['students']
    
    # Filter students with due assessments
    valid_students = [s for s in students if s.get('has_due', True)]
    
    if not valid_students:
        return {
            'total_students': len(students),
            'valid_students': 0,
            'average_completion': 0.0,
            'band_distribution': {},
            'top_performers': [],
            'needs_attention': []
        }
    
    completion_rates = [s['completion_rate'] for s in valid_students]
    average_completion = round(np.mean(completion_rates), 2)
    
    # Band distribution
    band_distribution = {}
    for student in valid_students:
        band = get_band(student['completion_rate'])
        band_distribution[band] = band_distribution.get(band, 0) + 1
    
    # Sort students by completion rate
    sorted_students = sorted(valid_students, key=lambda x: x['completion_rate'], reverse=True)
    
    # Top performers (90%+)
    top_performers = [s for s in sorted_students if s['completion_rate'] >= 90]
    
    # Needs attention (<60%)
    needs_attention = [s for s in sorted_students if s['completion_rate'] < 60]
    
    return {
        'total_students': len(students),
        'valid_students': len(valid_students),
        'average_completion': average_completion,
        'band_distribution': band_distribution,
        'top_performers': top_performers[:10],  # Top 10
        'needs_attention': needs_attention[:10]  # Top 10 who need attention
    }


def calculate_weekly_kpis(all_data):
    """
    Calculate weekly KPIs across all subjects.
    Excludes students/subjects with no due assessments (has_due=False).
    
    Args:
        all_data: List of all sheet data
    
    Returns:
        dict: Weekly KPIs
    """
    total_students = set()
    all_completion_rates = []
    subject_averages = []
    
    for sheet_data in all_data:
        valid_students = [s for s in sheet_data['students'] if s.get('has_due', True)]
        
        if not valid_students:
            continue
        
        for student in valid_students:
            total_students.add(student['student_name'])
            all_completion_rates.append(student['completion_rate'])
        
        # Calculate subject average
        class_stats = calculate_class_stats(sheet_data)
        if class_stats['valid_students'] > 0:
            subject_averages.append({
                'subject': sheet_data['sheet_name'],
                'average': class_stats['average_completion']
            })
    
    # Overall average (school_completion_avg)
    school_completion_avg = round(np.mean(all_completion_rates), 2) if all_completion_rates else 0.0
    
    # Calculate band distribution based on OVERALL student performance
    # (not per subject, but per student across all subjects)
    student_overall_stats = calculate_student_overall_stats(all_data)
    band_counts = {}
    for student_name, stats in student_overall_stats.items():
        band = stats['overall_band']
        if band != 'N/A':  # Exclude students with no valid data
            band_counts[band] = band_counts.get(band, 0) + 1
    
    # Top and bottom subjects
    sorted_subjects = sorted(subject_averages, key=lambda x: x['average'], reverse=True)
    top_subjects = sorted_subjects[:5]
    bottom_subjects = sorted_subjects[-5:]
    
    return {
        'total_students': len(total_students),
        'total_assessments': len(all_completion_rates),
        'school_completion_avg': school_completion_avg,
        'band_distribution': band_counts,
        'top_subjects': top_subjects,
        'bottom_subjects': bottom_subjects
    }


def create_dataframe_for_class(sheet_data):
    """
    Create a pandas DataFrame for a class/subject report.
    
    Args:
        sheet_data: Single sheet data dictionary
    
    Returns:
        pd.DataFrame: Formatted dataframe
    """
    rows = []
    
    for student in sheet_data['students']:
        completion_rate = student['completion_rate']
        band = get_band(completion_rate)
        emoji = get_band_emoji(band)
        
        rows.append({
            'اسم الطالب': student['student_name'],
            'المكتمل': student['completed'],
            'المطلوب': student['total_due'],
            'النسبة المئوية': f"{completion_rate:.1f}%" if student.get('has_due', True) else "N/A",
            'التصنيف': f"{emoji} {band}"
        })
    
    df = pd.DataFrame(rows)
    return df

