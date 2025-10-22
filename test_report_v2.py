"""
Test for comprehensive report - version 2
"""
from datetime import date
from pathlib import Path
from io import BytesIO

# Import modules
from enjaz.data_ingest_lms import aggregate_lms_files
from enjaz.comprehensive_report import create_comprehensive_report

# Mock file upload object
class MockUploadedFile:
    def __init__(self, filepath):
        self.name = Path(filepath).name
        with open(filepath, 'rb') as f:
            self._content = f.read()
        self._io = BytesIO(self._content)
    
    def read(self):
        return self._io.read()
    
    def seek(self, pos, whence=0):
        return self._io.seek(pos, whence)
    
    def tell(self):
        return self._io.tell()

# Create mock file
print("📁 Loading sample data...")
mock_file = MockUploadedFile('sample_data_correct.xlsx')

# Process data
today = date.today()
all_data = aggregate_lms_files([mock_file], today=today)

print(f"✅ Loaded {len(all_data)} sheets")

if len(all_data) > 0:
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
        
        print(f"\n📊 Sample data (first 3 rows):")
        print(df.head(3).to_string())
        
        print("\n✅ Test completed successfully!")
    else:
        print("⚠️ Report is empty")
else:
    print("⚠️ No data loaded from sample file")
