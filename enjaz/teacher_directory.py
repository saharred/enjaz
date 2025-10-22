"""
Teacher directory module for Enjaz application.
Handles teacher directory loading, validation, and merging.
"""

import pandas as pd
import re


def load_teacher_directory(file_path_or_buffer):
    """
    Load teacher directory from Excel file.
    
    Expected columns:
    - Teacher Name (اسم المعلم)
    - Email (البريد الإلكتروني)
    - Subject (المادة)
    - Class (الصف)
    
    Args:
        file_path_or_buffer: Path to Excel file or file buffer
    
    Returns:
        pd.DataFrame: Teacher directory with standardized columns
    """
    try:
        df = pd.read_excel(file_path_or_buffer)
        
        # Standardize column names
        column_mapping = {
            'Teacher Name': 'teacher_name',
            'اسم المعلم': 'teacher_name',
            'Email': 'email',
            'البريد الإلكتروني': 'email',
            'Subject': 'subject',
            'المادة': 'subject',
            'Class': 'class',
            'الصف': 'class'
        }
        
        # Rename columns
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df.rename(columns={old_name: new_name}, inplace=True)
        
        # Validate required columns
        required_cols = ['teacher_name', 'email', 'subject', 'class']
        missing = [col for col in required_cols if col not in df.columns]
        
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        # Clean and normalize data
        df['teacher_name'] = df['teacher_name'].str.strip()
        df['email'] = df['email'].str.strip().str.lower()
        df['subject'] = df['subject'].str.strip()
        df['class'] = df['class'].astype(str).str.strip()
        
        # Remove rows with missing data
        df = df.dropna(subset=['teacher_name', 'email'])
        
        return df
    
    except Exception as e:
        raise ValueError(f"Error loading teacher directory: {str(e)}")


def merge_teacher_directory(all_data, teacher_directory):
    """
    Merge teacher directory with assessment data.
    
    For each sheet (subject/class), find matching teachers and add their emails.
    If multiple teachers teach the same subject/class, concatenate emails with "; ".
    
    Args:
        all_data: List of sheet data from data_ingest
        teacher_directory: DataFrame from load_teacher_directory
    
    Returns:
        list: Updated all_data with teacher emails
    """
    for sheet_data in all_data:
        subject = sheet_data.get('subject', sheet_data['sheet_name'])
        class_code = sheet_data.get('class_code', '')
        
        # Find matching teachers
        matches = teacher_directory[
            (teacher_directory['subject'].str.contains(subject, case=False, na=False)) |
            (teacher_directory['class'].str.contains(class_code, case=False, na=False))
        ]
        
        if not matches.empty:
            # Concatenate emails with "; "
            emails = "; ".join(matches['email'].unique())
            teacher_names = "; ".join(matches['teacher_name'].unique())
            
            sheet_data['teacher_emails'] = emails
            sheet_data['teacher_names'] = teacher_names
        else:
            sheet_data['teacher_emails'] = None
            sheet_data['teacher_names'] = None
    
    return all_data


def filter_by_teacher_emails(all_data, selected_emails):
    """
    Filter assessment data to only include sheets taught by selected teachers.
    
    Args:
        all_data: List of sheet data with teacher_emails
        selected_emails: List of email addresses or single email string
    
    Returns:
        list: Filtered all_data
    """
    if isinstance(selected_emails, str):
        selected_emails = [selected_emails]
    
    # Normalize emails
    selected_emails = [email.strip().lower() for email in selected_emails]
    
    filtered_data = []
    
    for sheet_data in all_data:
        teacher_emails = sheet_data.get('teacher_emails', '')
        
        if not teacher_emails:
            continue
        
        # Split concatenated emails
        sheet_emails = [e.strip().lower() for e in teacher_emails.split(';')]
        
        # Check if any selected email is in sheet emails
        if any(email in sheet_emails for email in selected_emails):
            filtered_data.append(sheet_data)
    
    return filtered_data


def get_all_teacher_emails(all_data):
    """
    Get list of all unique teacher emails from data.
    
    Args:
        all_data: List of sheet data with teacher_emails
    
    Returns:
        list: Sorted list of unique email addresses
    """
    all_emails = set()
    
    for sheet_data in all_data:
        teacher_emails = sheet_data.get('teacher_emails', '')
        
        if teacher_emails:
            emails = [e.strip().lower() for e in teacher_emails.split(';')]
            all_emails.update(emails)
    
    return sorted(list(all_emails))

