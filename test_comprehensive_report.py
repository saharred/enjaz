"""
Test script for comprehensive report functionality
"""
import pandas as pd
from datetime import date
from enjaz.data_ingest_lms import aggregate_lms_files
from enjaz.comprehensive_report import create_comprehensive_report

# Load sample data
print("Loading sample data...")
with open('sample_data_correct.xlsx', 'rb') as f:
    files = [f]
    today = date.today()
    
    # Process data
    all_data = aggregate_lms_files([('sample_data_correct.xlsx', f.read())], today=today)

print(f"Loaded {len(all_data)} sheets")

# Create comprehensive report
print("\nCreating comprehensive report...")
df = create_comprehensive_report(all_data)

print(f"\nReport created with {len(df)} rows")
print(f"Unique students: {df['اسم الطالب'].nunique()}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nFirst 5 rows:")
print(df.head())

print("\n✅ Test completed successfully!")
