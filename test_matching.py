import sys
sys.path.insert(0, '/home/ubuntu/enjaz')
import pandas as pd
import re
from enjaz.data_ingest_lms import ingest_lms_data

# Load teacher data
teachers_df = pd.read_excel('بياناتالمعلمات.xlsx')
print("=== Teacher Data ===")
print(teachers_df.head())
print("\nColumns:", teachers_df.columns.tolist())
print("\nSample rows:")
for idx, row in teachers_df.head(3).iterrows():
    print(f"Teacher: {row.get('اسم المعلم', 'N/A')}")
    print(f"  Subject: {row.get('المادة', row.get('المادة الدراسية', 'N/A'))}")
    print(f"  Grade (raw): '{row.get('الصف', 'N/A')}'")
    grade_raw = str(row.get('الصف', '')).strip()
    grade_numbers = re.findall(r'\d+', grade_raw)
    grade = grade_numbers[0] if grade_numbers else grade_raw
    print(f"  Grade (extracted): '{grade}'")
    print(f"  Section: '{row.get('الشعبة', 'N/A')}'")
    print()

# Load student data
all_data = ingest_lms_data('ثالث1.xls')
print("\n=== Student Data ===")
print(f"Number of sheets: {len(all_data)}")
for sheet_data in all_data[:3]:
    print(f"Subject: '{sheet_data.get('subject', 'N/A')}'")
    print(f"Grade: '{sheet_data.get('grade', 'N/A')}'")
    print(f"Section: '{sheet_data.get('section', 'N/A')}'")
    print()

# Test matching
print("\n=== Testing Matches ===")
for idx, row in teachers_df.head(5).iterrows():
    teacher_name = row.get('اسم المعلم', 'N/A')
    subject = row.get('المادة', row.get('المادة الدراسية', ''))
    section = str(row.get('الشعبة', '')).strip()
    grade_raw = str(row.get('الصف', '')).strip()
    grade_numbers = re.findall(r'\d+', grade_raw)
    grade = grade_numbers[0] if grade_numbers else grade_raw
    
    print(f"\nTeacher: {teacher_name}")
    print(f"  Looking for: Subject='{subject}', Grade='{grade}', Section='{section}'")
    
    found = False
    for sheet_data in all_data:
        sheet_subject = sheet_data.get('subject', '').strip()
        sheet_section = str(sheet_data.get('section', '')).strip()
        sheet_grade = str(sheet_data.get('grade', '')).strip()
        
        if (subject.strip() == sheet_subject and 
            section == sheet_section and 
            grade == sheet_grade):
            print(f"  ✓ MATCH FOUND!")
            found = True
            break
    
    if not found:
        print(f"  ✗ NO MATCH")
        print(f"  Available in student data:")
        for sheet_data in all_data:
            print(f"    - Subject='{sheet_data.get('subject', '')}', Grade='{sheet_data.get('grade', '')}', Section='{sheet_data.get('section', '')}'")
        break  # Only show details for first non-match
