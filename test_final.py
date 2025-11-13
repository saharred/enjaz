import sys
sys.path.insert(0, '/home/ubuntu/enjaz')
import pandas as pd
import re
from enjaz.data_ingest_lms import parse_lms_excel

# Load teacher data
teachers_df = pd.read_excel('بياناتالمعلمات.xlsx')

# Load student data
all_data = parse_lms_excel('ثالث1.xls')

print("=== Available Data ===")
print(f"Teacher records: {len(teachers_df)}")
print(f"Student sheets: {len(all_data)}")

print("\n=== Student Data Sheets ===")
for sheet_data in all_data:
    print(f"  - Subject: '{sheet_data.get('subject', '')}', Grade: '{sheet_data.get('grade', '')}', Section: '{sheet_data.get('section', '')}'")

print("\n=== Testing Updated Matching Logic ===")
match_count = 0

for idx, row in teachers_df.iterrows():
    teacher_name = row.get('اسم المعلم', 'N/A')
    subject = str(row.get('المادة', row.get('المادة الدراسية', ''))).strip()
    section = str(row.get('الشعبة', '')).strip()
    grade_raw = str(row.get('الصف', '')).strip()
    
    # Extract grade number
    grade_numbers = re.findall(r'\d+', grade_raw)
    grade = grade_numbers[0] if grade_numbers else grade_raw
    
    # Check for match
    found = False
    for sheet_data in all_data:
        sheet_subject = sheet_data.get('subject', '').strip()
        sheet_section = str(sheet_data.get('section', '')).strip()
        sheet_grade = str(sheet_data.get('grade', '')).strip()
        
        if (subject.lower() == sheet_subject.lower() and 
            section == sheet_section and 
            grade == sheet_grade):
            found = True
            match_count += 1
            print(f"✓ {teacher_name}: {subject} - Grade {grade}, Section {section}")
            break

print(f"\n=== Results ===")
print(f"Total matches: {match_count} out of {len(teachers_df)} teachers")

if match_count == 0:
    print("\n⚠️ NO MATCHES FOUND!")
    print("This means the teacher data file contains different grades/sections than the student data file.")
    print("\nTeacher data sample (first 3):")
    for idx, row in teachers_df.head(3).iterrows():
        subject = str(row.get('المادة', row.get('المادة الدراسية', ''))).strip()
        grade_raw = str(row.get('الصف', '')).strip()
        section = str(row.get('الشعبة', '')).strip()
        grade_numbers = re.findall(r'\d+', grade_raw)
        grade = grade_numbers[0] if grade_numbers else grade_raw
        print(f"  - Subject: '{subject}', Grade: '{grade}', Section: '{section}'")
