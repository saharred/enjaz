"""
Direct test without mock objects
"""
import pandas as pd
from datetime import date
from enjaz.data_ingest_lms import parse_lms_excel
from enjaz.comprehensive_report import create_comprehensive_report

print("📁 Loading sample data...")
today = date.today()

# Parse directly
all_data = parse_lms_excel('sample_data_correct.xlsx', today=today)

print(f"✅ Loaded {len(all_data)} sheets")

if len(all_data) > 0:
    print(f"\n📊 First sheet info:")
    print(f"   - Subject: {all_data[0].get('subject', 'N/A')}")
    print(f"   - Grade: {all_data[0].get('grade', 'N/A')}")
    print(f"   - Students: {len(all_data[0].get('students', []))}")
    
    # Create comprehensive report
    print("\n📊 Creating comprehensive report...")
    df = create_comprehensive_report(all_data)
    
    if not df.empty:
        print(f"\n✅ Report created:")
        print(f"   - Total rows: {len(df)}")
        print(f"   - Unique students: {df['اسم الطالب'].nunique()}")
        print(f"   - Columns: {len(df.columns)}")
        
        print(f"\n📋 Column names:")
        for col in df.columns:
            print(f"   - {col}")
        
        print(f"\n📊 Sample (first 2 rows):")
        for idx, row in df.head(2).iterrows():
            print(f"\n   Row {idx}:")
            for col in df.columns:
                print(f"      {col}: {row[col]}")
        
        print("\n✅ Test completed successfully!")
    else:
        print("⚠️ Report is empty")
else:
    print("⚠️ No data loaded")
