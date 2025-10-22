"""
Data ingestion module for LMS Excel exports (actual format).
Handles the specific structure from Qatar LMS system.
"""

import pandas as pd
import numpy as np
from datetime import datetime, date
import re


def parse_lms_date(date_str):
    """
    Parse date from LMS format (e.g., 'Oct 31', 'Sep 30').
    
    Args:
        date_str: Date string from LMS
    
    Returns:
        date object or None
    """
    if pd.isna(date_str) or date_str == '-' or str(date_str).strip() == '':
        return None
    
    try:
        # Try parsing "Oct 31" format
        current_year = datetime.now().year
        parsed = datetime.strptime(f"{date_str} {current_year}", "%b %d %Y")
        return parsed.date()
    except:
        pass
    
    try:
        # Try other formats
        parsed = pd.to_datetime(date_str, dayfirst=True)
        return parsed.date()
    except:
        return None


def normalize_arabic_text(text):
    """Normalize Arabic text by removing extra whitespace."""
    if pd.isna(text):
        return ""
    
    text = str(text).strip()
    text = re.sub(r'\s+', ' ', text)
    return text


def parse_lms_excel(file_path_or_buffer, today=None, week_name="Week 1"):
    """
    Parse Excel file from Qatar LMS export format.
    
    Structure:
    - Row 0: Assignment titles
    - Row 1: Category
    - Row 2: Due dates
    - Row 3: Column labels (Students, M, I, AB, X, Overall, -, then scores)
    - Row 4+: Student data
    
    Args:
        file_path_or_buffer: Path to Excel file or file buffer
        today: Current date for filtering (date object)
        week_name: Name of the week/file
    
    Returns:
        list: Parsed data for all sheets
    """
    if today is None:
        import pytz
        qatar_tz = pytz.timezone('Asia/Qatar')
        today = datetime.now(qatar_tz).date()
    
    all_sheets_data = []
    
    try:
        # Try reading with xlrd for .xls files
        try:
            xls = pd.ExcelFile(file_path_or_buffer, engine='xlrd')
            engine = 'xlrd'
        except:
            # Fall back to openpyxl for .xlsx files
            xls = pd.ExcelFile(file_path_or_buffer, engine='openpyxl')
            engine = 'openpyxl'
        
        for sheet_name in xls.sheet_names:
            try:
                # Read sheet without headers
                df = pd.read_excel(
                    file_path_or_buffer,
                    sheet_name=sheet_name,
                    engine=engine,
                    header=None
                )
                
                if df.shape[0] < 5:
                    print(f"Skipping sheet '{sheet_name}': too few rows")
                    continue
                
                # Parse sheet name (e.g., "اللغة العربية 03 1" -> subject="اللغة العربية", class="03 1")
                parts = sheet_name.strip().split()
                if len(parts) >= 3:
                    subject = ' '.join(parts[:-2])
                    class_code = ' '.join(parts[-2:])
                else:
                    subject = sheet_name
                    class_code = "N/A"
                
                # Row 0: Headers (assignment titles)
                # Row 1: Category
                # Row 2: Due dates
                # Row 3: Labels (Students, M, I, AB, X, Overall, -, scores...)
                # Row 4+: Student data
                
                # Find assessment columns (starting from column 7, index 7)
                assessment_columns = []
                
                for col_idx in range(7, df.shape[1]):
                    header = df.iloc[0, col_idx]
                    due_str = df.iloc[2, col_idx]
                    
                    # Skip if header is empty or NaN
                    if pd.isna(header) or str(header).strip() == '':
                        continue
                    
                    # Parse due date
                    due_date = parse_lms_date(due_str)
                    
                    assessment_columns.append({
                        'col_idx': col_idx,
                        'title': str(header).strip(),
                        'due_date': due_date
                    })
                
                # Process student rows (starting from row 4, index 4)
                students_data = []
                
                for row_idx in range(4, df.shape[0]):
                    student_name_raw = df.iloc[row_idx, 0]  # Column 0 = Students
                    student_name = normalize_arabic_text(student_name_raw)
                    
                    # Skip rows without student name
                    if not student_name or student_name == 'Students':
                        continue
                    
                    # Count assessments for this student
                    total_due = 0
                    completed = 0
                    not_submitted = 0
                    student_assessments = []
                    
                    for assessment in assessment_columns:
                        col_idx = assessment['col_idx']
                        due_date = assessment['due_date']
                        
                        # Only consider assessments with due_date <= today
                        if due_date is None or due_date > today:
                            continue
                        
                        total_due += 1
                        
                        # Get cell value
                        cell_value = df.iloc[row_idx, col_idx]
                        
                        # Determine status
                        if pd.isna(cell_value) or str(cell_value).strip() in ['', '-']:
                            status = 'empty'
                        elif str(cell_value).upper() == 'M':
                            status = 'M'
                            not_submitted += 1
                        elif str(cell_value).upper() in ['I', 'AB', 'X']:
                            status = 'excluded'
                        else:
                            # Try to parse as number
                            try:
                                score = float(cell_value)
                                if 0 <= score <= 100:
                                    status = 'completed'
                                    completed += 1
                                else:
                                    status = 'invalid'
                            except:
                                status = 'invalid'
                        
                        student_assessments.append({
                            'title': assessment['title'],
                            'due_date': due_date.isoformat() if due_date else None,
                            'value': str(cell_value) if pd.notna(cell_value) else '',
                            'status': status
                        })
                    
                    # Calculate completion rate
                    if total_due > 0:
                        completion_rate = round(100.0 * completed / total_due, 2)
                        has_due = True
                    else:
                        completion_rate = 0.0
                        has_due = False
                    
                    students_data.append({
                        'student_name': student_name,
                        'total_due': total_due,
                        'completed': completed,
                        'not_submitted': not_submitted,
                        'completion_rate': completion_rate,
                        'has_due': has_due,
                        'assessments': student_assessments
                    })
                
                # Store sheet data
                if students_data:
                    all_sheets_data.append({
                        'sheet_name': sheet_name,
                        'subject': subject,
                        'class_code': class_code,
                        'week_name': week_name,
                        'students': students_data
                    })
                    print(f"✅ Processed sheet '{sheet_name}': {len(students_data)} students")
                
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


def aggregate_lms_files(uploaded_files, today=None, start_date=None, end_date=None):
    """
    Aggregate data from multiple LMS Excel files.
    
    Args:
        uploaded_files: List of uploaded file objects
        today: Current date for due date comparison (date object) - deprecated, use end_date
        start_date: Start date for filtering assessments (date object)
        end_date: End date for filtering assessments (date object)
    
    Returns:
        list: Combined data from all files
    """
    all_data = []
    
    # Use end_date if provided, otherwise use today
    filter_date = end_date if end_date is not None else today
    if filter_date is None:
        filter_date = date.today()
    
    for idx, uploaded_file in enumerate(uploaded_files):
        week_name = uploaded_file.name if hasattr(uploaded_file, 'name') else f"Week {idx + 1}"
        
        file_data = parse_lms_excel(
            uploaded_file, 
            today=filter_date, 
            week_name=week_name,
            start_date=start_date
        )
        all_data.extend(file_data)
    
    return all_data

