"""
Data ingestion module for Enjaz application.
Handles Excel file parsing and data extraction.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import pytz


def parse_excel_file(file_path_or_buffer, week_name=None):
    """
    Parse a single Excel file containing multiple sheets (subjects/classes).
    
    Args:
        file_path_or_buffer: Path to Excel file or file buffer
        week_name: Optional name for the week (default: filename)
    
    Returns:
        list: List of dictionaries containing parsed data for each sheet
    """
    qatar_tz = pytz.timezone('Asia/Qatar')
    today = datetime.now(qatar_tz).date()
    
    all_sheets_data = []
    
    try:
        # Read all sheets
        excel_file = pd.ExcelFile(file_path_or_buffer)
        
        for sheet_name in excel_file.sheet_names:
            try:
                # Read the sheet
                df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
                
                if df.empty or df.shape[0] < 4:
                    continue
                
                # Extract assessment columns (starting from column H = index 7)
                assessment_start_col = 7
                
                # Row 1 (index 0) = assessment titles
                # Row 3 (index 2) = due dates
                # Row 4+ (index 3+) = student data
                
                assessment_titles = df.iloc[0, assessment_start_col:].values
                due_dates_raw = df.iloc[2, assessment_start_col:].values
                
                # Parse due dates
                due_dates = []
                for dd in due_dates_raw:
                    if pd.isna(dd):
                        due_dates.append(None)
                    else:
                        try:
                            if isinstance(dd, datetime):
                                due_dates.append(dd.date())
                            elif isinstance(dd, str):
                                parsed_date = pd.to_datetime(dd).date()
                                due_dates.append(parsed_date)
                            else:
                                due_dates.append(None)
                        except:
                            due_dates.append(None)
                
                # Process student rows (starting from row 4, index 3)
                students_data = []
                
                for idx in range(3, df.shape[0]):
                    student_name = df.iloc[idx, 0]  # Assuming column A (index 0) has student names
                    
                    if pd.isna(student_name) or str(student_name).strip() == '':
                        continue
                    
                    # Process assessments for this student
                    assessments = []
                    total_assigned_due = 0
                    not_submitted = 0
                    
                    for col_idx, (title, due_date) in enumerate(zip(assessment_titles, due_dates)):
                        actual_col = assessment_start_col + col_idx
                        
                        if actual_col >= df.shape[1]:
                            break
                        
                        value = df.iloc[idx, actual_col]
                        
                        # Skip if column is "Overall" or assessment title contains ignore keywords
                        if pd.notna(title) and ('Overall' in str(title) or 'overall' in str(title)):
                            continue
                        
                        # Check if due date is valid and <= today
                        if due_date is None or due_date > today:
                            continue
                        
                        total_assigned_due += 1
                        
                        # Check value
                        if pd.isna(value):
                            continue
                        
                        value_str = str(value).strip().upper()
                        
                        # M = not submitted
                        if value_str == 'M':
                            not_submitted += 1
                        # I, AB, X = ignore
                        elif value_str in ['I', 'AB', 'X']:
                            total_assigned_due -= 1  # Don't count this assessment
                        # Numeric = submitted (even if 0)
                        else:
                            try:
                                float(value_str)
                                # It's a number, counts as submitted
                            except ValueError:
                                # Not a number, not M, not I/AB/X - treat as submitted
                                pass
                        
                        assessments.append({
                            'title': title,
                            'due_date': due_date,
                            'value': value
                        })
                    
                    # Calculate completion rate
                    if total_assigned_due > 0:
                        completed = total_assigned_due - not_submitted
                        completion_rate = 100 * completed / total_assigned_due
                    else:
                        completed = 0
                        completion_rate = None  # N/A
                    
                    students_data.append({
                        'student_name': str(student_name).strip(),
                        'total_assigned_due': total_assigned_due,
                        'completed': completed,
                        'not_submitted': not_submitted,
                        'completion_rate': completion_rate,
                        'assessments': assessments
                    })
                
                # Store sheet data
                all_sheets_data.append({
                    'sheet_name': sheet_name,
                    'week_name': week_name,
                    'students': students_data
                })
                
            except Exception as e:
                print(f"Error processing sheet {sheet_name}: {str(e)}")
                continue
    
    except Exception as e:
        print(f"Error reading Excel file: {str(e)}")
        return []
    
    return all_sheets_data


def aggregate_multiple_files(uploaded_files):
    """
    Aggregate data from multiple uploaded Excel files.
    
    Args:
        uploaded_files: List of uploaded file objects
    
    Returns:
        list: Combined data from all files
    """
    all_data = []
    
    for idx, uploaded_file in enumerate(uploaded_files):
        week_name = uploaded_file.name if hasattr(uploaded_file, 'name') else f"Week {idx + 1}"
        file_data = parse_excel_file(uploaded_file, week_name=week_name)
        all_data.extend(file_data)
    
    return all_data

