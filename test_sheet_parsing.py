import sys
sys.path.insert(0, '/home/ubuntu/enjaz')

# Test the parsing logic
test_cases = [
    "التربية الاسلامية 1 03",  # Section first, grade second
    "اللغة العربية 03 1",      # Grade first, section second
    "الرياضيات 2 04",
    "العلوم 05 3"
]

for sheet_name in test_cases:
    parts = sheet_name.strip().split()
    subject = ' '.join(parts[:-2])
    class_parts = parts[-2:]
    
    first_num = class_parts[0]
    second_num = class_parts[1]
    
    if first_num.startswith('0') or (first_num.isdigit() and int(first_num) > 9):
        class_name = first_num
        section = second_num
        format_type = "grade first"
    else:
        class_name = second_num
        section = first_num
        format_type = "section first"
    
    # Normalize grade
    normalized_grade = str(int(class_name)) if class_name.isdigit() else class_name
    
    print(f"Sheet: '{sheet_name}'")
    print(f"  → Subject: '{subject}', Grade: '{normalized_grade}', Section: '{section}' ({format_type})")
    print()
