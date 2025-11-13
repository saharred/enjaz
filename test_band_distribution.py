"""
Test band distribution calculation.
"""

from datetime import date
from enjaz.data_ingest import parse_excel_file
from enjaz.analysis import calculate_weekly_kpis, calculate_student_overall_stats

# Test with the actual file
file_path = '/home/ubuntu/upload/grades_1761219323.xls'

print("Testing band distribution calculation...")
print("=" * 70)

# Parse the file
today = date.today()
all_data = parse_excel_file(file_path, today=today, week_name="Test Week")

# Calculate KPIs
kpis = calculate_weekly_kpis(all_data)

print(f"\nTotal students: {kpis['total_students']}")
print(f"\nBand distribution:")
print("=" * 70)

total_in_bands = 0
for band, count in sorted(kpis['band_distribution'].items(), key=lambda x: x[1], reverse=True):
    total_in_bands += count
    print(f"{band:30} {count:3} طالب ({count/kpis['total_students']*100:.1f}%)")

print("=" * 70)
print(f"Total students in bands: {total_in_bands}")
print(f"Expected total students: {kpis['total_students']}")

if total_in_bands == kpis['total_students']:
    print("\n✅ SUCCESS: Band distribution matches total students!")
else:
    print(f"\n❌ ERROR: Missing {kpis['total_students'] - total_in_bands} students from band distribution!")

# Show individual student stats
print("\n" + "=" * 70)
print("Individual student overall stats:")
print("=" * 70)

student_stats = calculate_student_overall_stats(all_data)
for idx, (name, stats) in enumerate(sorted(student_stats.items(), key=lambda x: x[1]['overall_completion_rate'], reverse=True), 1):
    print(f"{idx:2}. {name:40} {stats['overall_completion_rate']:6.1f}% - {stats['overall_band']}")

print("\n" + "=" * 70)
print("Testing complete!")

