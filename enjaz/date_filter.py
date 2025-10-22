"""
Date range filtering module for Enjaz application.
Allows filtering assessments by date range.
"""

from datetime import date


def filter_by_date_range(all_data, start_date=None, end_date=None):
    """
    Filter assessment data to only include assessments within date range.
    Recomputes all metrics (total_due, completed, completion_rate) based on filtered assessments.
    
    Args:
        all_data: List of sheet data from data_ingest
        start_date: Start date (inclusive), None means no start limit
        end_date: End date (inclusive), None means no end limit
    
    Returns:
        list: New all_data with recomputed metrics
    """
    filtered_data = []
    
    for sheet_data in all_data:
        # Create a copy to avoid modifying original
        new_sheet_data = sheet_data.copy()
        new_students = []
        
        for student in sheet_data['students']:
            # Recount assessments within date range
            total_due = 0
            completed = 0
            not_submitted = 0
            
            # Get original assessments if available
            assessments = student.get('assessments', [])
            
            if not assessments:
                # If no detailed assessments, keep original counts
                # (This shouldn't happen with new data_ingest, but keep for compatibility)
                new_students.append(student.copy())
                continue
            
            # Filter and recount
            for assessment in assessments:
                due_date = assessment.get('due_date')
                
                if due_date is None:
                    continue
                
                # Check if within date range
                if start_date and due_date < start_date:
                    continue
                if end_date and due_date > end_date:
                    continue
                
                # This assessment is within range
                total_due += 1
                
                value = assessment.get('value')
                
                if pd.isna(value):
                    not_submitted += 1
                    continue
                
                value_str = str(value).strip().upper()
                
                if value_str == 'M':
                    not_submitted += 1
                elif value_str in ['I', 'AB', 'X']:
                    total_due -= 1  # Don't count
                else:
                    completed += 1
            
            # Recalculate completion rate
            has_due = total_due > 0
            
            if has_due:
                completion_rate = round(100 * completed / total_due, 2)
            else:
                completion_rate = 0.0
            
            # Create new student record
            new_student = student.copy()
            new_student['total_due'] = total_due
            new_student['completed'] = completed
            new_student['not_submitted'] = not_submitted
            new_student['completion_rate'] = completion_rate
            new_student['has_due'] = has_due
            
            new_students.append(new_student)
        
        new_sheet_data['students'] = new_students
        filtered_data.append(new_sheet_data)
    
    return filtered_data


# Import pandas for value checking
import pandas as pd

