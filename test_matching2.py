import sys
sys.path.insert(0, '/home/ubuntu/enjaz')
import pandas as pd
import re
from enjaz.data_ingest_lms import parse_lms_excel

# Load teacher data
teachers_df = pd.read_excel('بياناتالمعلمات.xlsx')
print("=== Teacher Data ===")
print(f"Total teachers: {len(teachers_df)}")
print("\nColumns:", teachers_df.columns.tolist())
print("\nFirst 3 rows:")
for idx, row in teachers_df.head(3).iterrows():
    teacher_name = row.get('اسم المعلم', 'N/A')
    subject = row.get('المادة', row.get('المادة الدراسية', 'N/A'))
    grade_raw = str(row.get('الصف', 'N/A')).strip()
    section = str(row.get('الشعبة', 'N/A')).strip()
    
    # Extract grade number from text like "ثالث3" -> "3"
    grade_numbers = re.findall(r'\d+', grade_raw)
    grade = grade_numbers[0] if grade_numbers else grade_raw
    
    print(f"\nTeacher: {teacher_name}")
    print(f"  Subject: '{subject}'")
    print(f"  Grade (raw): '{grade_raw}' → (extracted): '{grade}'")
    print(f"  Section: '{section}'")

# Load student data
print("\n\n=== Student Data ===")
all_data = parse_lms_excel('ثالث1.xls')
print(f"Number of sheets: {len(all_data)}")
for sheet_data in all_data[:5]:
    print(f"\nSheet: {sheet_data.get('sheet_name', 'N/A')}")
    print(f"  Subject: '{sheet_data.get('subject', 'N/A')}'")
    print(f"  Grade: '{sheet_data.get('grade', 'N/A')}'")
    print(f"  Section: '{sheet_data.get('section', 'N/A')}'")

# Test matching
print("\n\n=== Testing Matches ===")
match_count = 0
for idx, row in teachers_df.iterrows():
    teacher_name = row.get('اسم المعلم', 'N/A')
    subject = row.get('المادة', row.get('المادة الدراسية', ''))
    section = str(row.get('الشعبة', '')).strip()
    grade_raw = str(row.get('الصف', '')).strip()
    grade_numbers = re.findall(r'\d+', grade_raw)
    grade = grade_numbers[0] if grade_numbers else grade_raw
    
    found = False
    for sheet_data in all_data:
        sheet_subject = sheet_data.get('subject', '').strip()
        sheet_section = str(sheet_data.get('section', '')).strip()
        sheet_grade = str(sheet_data.get('grade', '')).strip()
        
        if (subject.strip() == sheet_subject and 
            section == sheet_section and 
            grade == sheet_grade):
            found = True
            match_count += 1
            print(f"✓ {teacher_name}: Subject='{subject}', Grade='{grade}', Section='{section}'")
            break
    
    if not found and idx < 3:  # Show details for first 3 non-matches
        print(f"\n✗ {teacher_name}: NO MATCH")
        print(f"  Looking for: Subject='{subject}', Grade='{grade}', Section='{section}'")
        print(f"  Available sheets:")
        for sheet_data in all_data[:3]:
            print(f"    - Subject='{sheet_data.get('subject', '')}', Grade='{sheet_data.get('grade', '')}', Section='{sheet_data.get('section', '')}'")

print(f"\n\nTotal matches: {match_count} out of {len(teachers_df)} teachers")
