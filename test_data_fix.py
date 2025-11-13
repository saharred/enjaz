"""
Test script to verify data processing fixes.
"""

import sys
from datetime import date
from enjaz.data_ingest import parse_excel_file

# Test with the actual file
file_path = '/home/ubuntu/upload/grades_1761219323.xls'

print("Testing data processing with actual file...")
print("=" * 70)

# Parse the file
today = date.today()
all_data = parse_excel_file(file_path, today=today, week_name="Test Week")

print(f"\nTotal sheets processed: {len(all_data)}")

# Find the student "السماني كمال السماني الحاج"
target_student = "السماني كمال السماني الحاج"

print(f"\nLooking for student: {target_student}")
print("=" * 70)

for sheet_data in all_data:
    subject = sheet_data['subject']
    
    for student in sheet_data['students']:
        if target_student in student['student_name']:
            print(f"\n📚 Subject: {subject}")
            print(f"   Total Due: {student['total_due']}")
            print(f"   Completed: {student['completed']}")
            print(f"   Not Submitted: {student['not_submitted']}")
            print(f"   Completion Rate: {student['completion_rate']}%")
            print(f"   Has Due: {student['has_due']}")
            
            # Show detailed assessments
            if student.get('assessments'):
                print(f"\n   Detailed Assessments:")
                for idx, assessment in enumerate(student['assessments'], 1):
                    print(f"      {idx}. {assessment['title']}: {assessment['value']}")

print("\n" + "=" * 70)
print("Testing complete!")

