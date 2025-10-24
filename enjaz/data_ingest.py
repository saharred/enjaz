"""
Data ingestion module for Enjaz application.
Handles Excel file parsing and data extraction.

Implements exact parsing rules as specified.
"""

import pandas as pd
import numpy as np
from datetime import datetime, date
import re


def find_student_name_column(df):
    """
    Find the student name column.
    Priority: first header containing "اسم" or "Student", else first column.
    
    Args:
        df: DataFrame with headers in first row
    
    Returns:
        int: Column index for student names
    """
    headers = df.iloc[0].astype(str)
    
    for idx, header in enumerate(headers):
        if 'اسم' in header or 'Student' in header.lower():
            return idx
    
    return 0  # Default to first column


def find_assessment_start_column(df):
    """
    Find where assessment columns start.
    Start at H (index 7) OR first column after "Overall", whichever is later.
    
    Note: This finds the starting point. Individual columns with "Overall"
    are still excluded via is_excluded_column().
    
    Args:
        df: DataFrame with headers in first row
    
    Returns:
        int: Starting column index for assessments
    """
    headers = df.iloc[0].astype(str)
    
    # Default start: column H (index 7)
    start_col = 7
    
    # Find last "Overall" column - if found BEFORE column H, start after it
    for idx, header in enumerate(headers):
        if idx < 7:  # Only check columns before H
            if 'Overall' in header or 'overall' in header or 'إجمالي' in header or 'المجموع' in header:
                start_col = max(start_col, idx + 1)
    
    return start_col


def is_excluded_column(header):
    """
    Check if a column should be excluded from assessment counting.
    
    Args:
        header: Column header string
    
    Returns:
        bool: True if should be excluded
    """
    header_str = str(header).lower()
    
    exclude_keywords = [
        'overall', 'unnamed', 'notes', 'ملاحظات', 
        'إجمالي', 'المجموع', 'nan'
    ]
    
    for keyword in exclude_keywords:
        if keyword in header_str:
            return True
    
    return False


def parse_due_date(value, dayfirst=True):
    """
    Parse due date from various formats.
    
    Args:
        value: Date value (can be datetime, string, or other)
        dayfirst: Whether to interpret dates as day-first
    
    Returns:
        date or None: Parsed date or None if invalid
    """
    if pd.isna(value):
        return None
    
    # Already a datetime
    if isinstance(value, (datetime, pd.Timestamp)):
        return value.date()
    
    # Already a date
    if isinstance(value, date):
        return value
    
    # Try parsing as string
    if isinstance(value, str):
        value = value.strip()
        
        # Arabic month names mapping
        arabic_months = {
            'يناير': 1, 'فبراير': 2, 'مارس': 3, 'أبريل': 4,
            'مايو': 5, 'يونيو': 6, 'يوليو': 7, 'أغسطس': 8,
            'سبتمبر': 9, 'أكتوبر': 10, 'نوفمبر': 11, 'ديسمبر': 12
        }
        
        # Try to parse Arabic date format: "شهر يوم" (e.g., "سبتمبر 30")
        for month_name, month_num in arabic_months.items():
            if month_name in value:
                # Extract day number
                day_str = value.replace(month_name, '').strip()
                try:
                    day = int(day_str)
                    # Use current year
                    current_year = datetime.now().year
                    return date(current_year, month_num, day)
                except (ValueError, TypeError):
                    pass
        
        # Try pandas parser with dayfirst
        try:
            parsed = pd.to_datetime(value, dayfirst=dayfirst, errors='coerce')
            if pd.notna(parsed):
                return parsed.date()
        except:
            pass
    
    return None


def parse_sheet_name(sheet_name):
    """
    Parse sheet name to extract subject and class.
    Examples:
        '03/1 Arabic' → ('Arabic', '03/1')
        'Arabic 03/1' → ('Arabic', '03/1')
    
    Args:
        sheet_name: Sheet name string
    
    Returns:
        tuple: (subject, class_code)
    """
    # Pattern: digits/digits or digits-digits
    class_pattern = r'\d+[/-]\d+'
    
    match = re.search(class_pattern, sheet_name)
    
    if match:
        class_code = match.group()
        # Remove class code from sheet name to get subject
        subject = sheet_name.replace(class_code, '').strip()
        return (subject, class_code)
    
    # No class code found
    return (sheet_name, '')


def normalize_arabic_text(text):
    """
    Normalize Arabic text by trimming and removing extra whitespace.
    
    Args:
        text: Input text
    
    Returns:
        str: Normalized text
    """
    if pd.isna(text):
        return ''
    
    text = str(text).strip()
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text


def parse_excel_file(file_path_or_buffer, today, week_name=None):
    """
    Parse a single Excel file containing multiple sheets (subjects/classes).
    
    Args:
        file_path_or_buffer: Path to Excel file or file buffer
        today: Current date for due date comparison (date object)
        week_name: Optional name for the week (default: filename)
    
    Returns:
        list: List of dictionaries containing parsed data for each sheet
    """
    all_sheets_data = []
    
    try:
        # Read all sheets
        excel_file = pd.ExcelFile(file_path_or_buffer)
        
        for sheet_name in excel_file.sheet_names:
            try:
                # Read the sheet without header
                df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
                
                if df.empty or df.shape[0] < 4:
                    print(f"Warning: Sheet '{sheet_name}' has insufficient rows, skipping.")
                    continue
                
                # Find student name column
                student_col = find_student_name_column(df)
                
                # Find assessment start column
                assessment_start = find_assessment_start_column(df)
                
                # Row 3 (index 2) contains due dates
                due_dates_row = df.iloc[2]
                
                # Get assessment columns (from assessment_start onward)
                assessment_columns = []
                
                for col_idx in range(assessment_start, df.shape[1]):
                    header = df.iloc[0, col_idx]
                    
                    # Skip excluded columns
                    if is_excluded_column(header):
                        continue
                    
                    # Parse due date
                    due_date_value = due_dates_row.iloc[col_idx]
                    due_date = parse_due_date(due_date_value, dayfirst=True)
                    
                    assessment_columns.append({
                        'col_idx': col_idx,
                        'title': str(header) if pd.notna(header) else f'Assessment {col_idx}',
                        'due_date': due_date
                    })
                
                # Process student rows (starting from row 4, index 3)
                students_data = []
                
                for row_idx in range(3, df.shape[0]):
                    student_name_raw = df.iloc[row_idx, student_col]
                    student_name = normalize_arabic_text(student_name_raw)
                    
                    # Skip rows without student name
                    if not student_name:
                        continue
                    
                    # Count assessments for this student
                    total_due = 0
                    completed = 0
                    not_submitted = 0
                    student_assessments = []  # Store detailed assessment info
                    
                    for assessment in assessment_columns:
                        col_idx = assessment['col_idx']
                        due_date = assessment['due_date']
                        
                        # Only consider assessments with due_date <= today
                        if due_date is None or due_date > today:
                            continue
                        
                        total_due += 1
                        
                        # Get cell value
                        cell_value = df.iloc[row_idx, col_idx]
                        
                        if pd.isna(cell_value):
                            # Empty cell - not submitted
                            not_submitted += 1
                            continue
                        
                        value_str = str(cell_value).strip().upper()
                        
                        # Store assessment details
                        student_assessments.append({
                            'title': assessment['title'],
                            'due_date': due_date,
                            'value': cell_value
                        })
                        
                        if value_str in ['M', 'I', 'AB', 'X']:
                            # Not submitted (M/I/AB/X all count as 0%)
                            not_submitted += 1
                        else:
                            # Submitted (numeric or any other value)
                            completed += 1
                    
                    # Calculate completion rate
                    has_due = total_due > 0
                    
                    if has_due:
                        completion_rate = round(100 * completed / total_due, 2)
                    else:
                        completion_rate = 0.0
                    
                    students_data.append({
                        'student_name': student_name,
                        'total_due': total_due,
                        'completed': completed,
                        'not_submitted': not_submitted,
                        'completion_rate': completion_rate,
                        'has_due': has_due,
                        'assessments': student_assessments  # Include detailed assessments
                    })
                
                # Parse sheet name
                subject, class_code = parse_sheet_name(sheet_name)
                
                # Store sheet data
                if students_data:
                    all_sheets_data.append({
                        'sheet_name': sheet_name,
                        'subject': subject,
                        'class_code': class_code,
                        'week_name': week_name,
                        'students': students_data
                    })
                
            except Exception as e:
                import streamlit as st
                st.warning(f"⚠️ خطأ في معالجة الورقة '{sheet_name}': {str(e)}")
                print(f"Error processing sheet '{sheet_name}': {str(e)}")
                continue
    
    except Exception as e:
        import streamlit as st
        st.error(f"❌ خطأ في قراءة ملف Excel: {str(e)}")
        print(f"Error reading Excel file: {str(e)}")
        return []
    
    return all_sheets_data


def aggregate_multiple_files(uploaded_files, today):
    """
    Aggregate data from multiple uploaded Excel files.
    
    Args:
        uploaded_files: List of uploaded file objects
        today: Current date for due date comparison (date object)
    
    Returns:
        list: Combined data from all files
    """
    all_data = []
    
    for idx, uploaded_file in enumerate(uploaded_files):
        week_name = uploaded_file.name if hasattr(uploaded_file, 'name') else f"Week {idx + 1}"
        
        file_data = parse_excel_file(uploaded_file, today=today, week_name=week_name)
        all_data.extend(file_data)
    
    return all_data

