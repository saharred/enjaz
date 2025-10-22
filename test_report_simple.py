"""
Simple test for comprehensive report
"""
import sys
from datetime import date
from pathlib import Path

# Mock file upload object
class MockUploadedFile:
    def __init__(self, filepath):
        self.name = Path(filepath).name
        self.filepath = filepath
    
    def read(self):
        with open(self.filepath, 'rb') as f:
            return f.read()
    
    def seek(self, pos):
        pass

# Import modules
from enjaz.data_ingest_lms import aggregate_lms_files
from enjaz.comprehensive_report import create_comprehensive_report

# Create mock file
print("📁 Loading sample data...")
mock_file = MockUploadedFile('sample_data_correct.xlsx')

# Process data
today = date.today()
all_data = aggregate_lms_files([mock_file], today=today)

print(f"✅ Loaded {len(all_data)} sheets")

# Create comprehensive report
print("\n📊 Creating comprehensive report...")
df = create_comprehensive_report(all_data)

print(f"\n✅ Report created:")
print(f"   - Total rows: {len(df)}")
print(f"   - Unique students: {df['اسم الطالب'].nunique()}")
print(f"   - Columns: {len(df.columns)}")

print(f"\n📋 Column names:")
for col in df.columns:
    print(f"   - {col}")

print(f"\n📊 Sample data (first 3 rows):")
print(df.head(3).to_string())

print("\n✅ Test completed successfully!")
