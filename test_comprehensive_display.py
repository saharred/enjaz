"""Test script to display comprehensive report"""
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

# Add enjaz to path
sys.path.insert(0, str(Path(__file__).parent))

from enjaz.data_ingest_lms import aggregate_lms_files
from enjaz.comprehensive_report import create_comprehensive_report

# Use sample file
sample_file = Path(__file__).parent / 'sample_data_correct.xlsx'

if not sample_file.exists():
    print("❌ Sample file not found")
    sys.exit(1)

print("📂 Loading sample data...")
today = datetime.now()
all_data = aggregate_lms_files([str(sample_file)], today)

print(f"✅ Loaded {len(all_data)} sheets\n")

print("📊 Creating comprehensive report...")
df = create_comprehensive_report(all_data)

print(f"✅ Report created with {len(df)} rows\n")

print("=" * 120)
print("📋 التقرير التحليلي الشامل")
print("=" * 120)
print()

# Display column names
print("الأعمدة المتوفرة:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")
print()

# Display summary
print("📊 ملخص التقرير:")
print(f"  • عدد الطلاب: {df['اسم الطالب'].nunique()}")
print(f"  • عدد المواد: {df['المادة'].nunique()}")
print(f"  • إجمالي الصفوف: {len(df)}")
print()

# Display first 15 rows with all columns
print("=" * 150)
print("📋 أول 15 صف من التقرير (جميع الأعمدة):")
print("=" * 150)
print()

# Set pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 40)

print(df.head(15).to_string(index=False))
print()

# Display statistics by band
print("=" * 120)
print("📊 توزيع الطلاب حسب الفئات:")
print("=" * 120)
print()

# Get unique students with their bands
student_bands = df.groupby('اسم الطالب')['الفئة'].first()
band_counts = student_bands.value_counts()

for band, count in band_counts.items():
    print(f"  {band}: {count} طالب")
print()

# Display average completion by subject
print("=" * 120)
print("📊 متوسط الإنجاز حسب المادة:")
print("=" * 120)
print()

subject_avg = df.groupby('المادة')['نسبة الإنجاز للمادة (%)'].mean().sort_values(ascending=False)

for subject, avg in subject_avg.items():
    print(f"  {subject}: {avg:.1f}%")
print()

print("=" * 120)
print("✅ انتهى العرض التحليلي الشامل")
print("=" * 120)
