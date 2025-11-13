"""
Find students without due assessments.
"""

from datetime import date
from enjaz.data_ingest import parse_excel_file

# Test with the actual file
file_path = '/home/ubuntu/upload/grades_1761219323.xls'

print("Finding students without due assessments...")
print("=" * 70)

# Parse the file
today = date.today()
all_data = parse_excel_file(file_path, today=today, week_name="Test Week")

# Collect all unique students
all_students = set()
students_with_due = set()
students_without_due = set()

for sheet_data in all_data:
    for student in sheet_data['students']:
        student_name = student['student_name']
        all_students.add(student_name)
        
        if student.get('has_due', False):
            students_with_due.add(student_name)

# Find students without any due assessments across all subjects
students_without_due = all_students - students_with_due

print(f"\nTotal unique students: {len(all_students)}")
print(f"Students with due assessments: {len(students_with_due)}")
print(f"Students without due assessments: {len(students_without_due)}")

if students_without_due:
    print("\n" + "=" * 70)
    print("Students without any due assessments:")
    print("=" * 70)
    for idx, student in enumerate(sorted(students_without_due), 1):
        print(f"{idx}. {student}")
        
        # Show their data across all subjects
        print(f"   Subject breakdown:")
        for sheet_data in all_data:
            for s in sheet_data['students']:
                if s['student_name'] == student:
                    subject = sheet_data['subject']
                    print(f"      - {subject}: total_due={s['total_due']}, has_due={s.get('has_due', False)}")
        print()

print("\n" + "=" * 70)
print("Analysis complete!")

