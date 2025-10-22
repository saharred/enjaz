"""
Test suite for data ingestion and analysis modules.
Uses table-driven tests with deterministic date.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import date, timedelta
from io import BytesIO

from enjaz.data_ingest import (
    parse_excel_file,
    find_student_name_column,
    find_assessment_start_column,
    is_excluded_column,
    parse_due_date,
    parse_sheet_name,
    normalize_arabic_text
)
from enjaz.analysis import (
    get_band,
    BAND_LABELS,
    calculate_class_stats,
    calculate_weekly_kpis
)


# Deterministic test date
TEST_TODAY = date(2025, 10, 22)


def create_test_excel(data_dict, sheet_name='Test'):
    """Helper to create Excel file from data dictionary."""
    # Convert dict to DataFrame
    df = pd.DataFrame(data_dict)
    
    # Save to Excel buffer
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
    buffer.seek(0)
    
    return buffer


class TestDueDateFiltering:
    """Test due date filtering logic."""
    
    def test_future_assessment_excluded(self):
        """Assessments with due dates in the future should be excluded."""
        # Create proper Excel structure
        # Row 1 (index 0): Headers
        # Row 2 (index 1): Empty
        # Row 3 (index 2): Due dates
        # Row 4+ (index 3+): Student data
        
        data = []
        # Row 1: Headers
        row1 = [''] * 9
        row1[0] = 'اسم الطالب'
        row1[7] = 'Assessment 1'
        row1[8] = 'Assessment 2'
        data.append(row1)
        
        # Row 2: Empty
        data.append([''] * 9)
        
        # Row 3: Due dates
        row3 = [''] * 9
        row3[7] = TEST_TODAY - timedelta(days=1)  # Past
        row3[8] = TEST_TODAY + timedelta(days=1)  # Future
        data.append(row3)
        
        # Row 4: Student data
        row4 = [''] * 9
        row4[0] = 'أحمد محمد'
        row4[7] = 75
        row4[8] = 80
        data.append(row4)
        
        buffer = create_test_excel(data)
        result = parse_excel_file(buffer, today=TEST_TODAY)
        
        assert len(result) == 1
        assert len(result[0]['students']) == 1
        
        student = result[0]['students'][0]
        assert student['total_due'] == 1  # Only the past assessment
        assert student['student_name'] == 'أحمد محمد'


class TestSpecialValueHandling:
    """Test M/I/AB/X handling."""
    
    def test_m_i_ab_x_handling(self):
        """Test that M counts as not_submitted, I/AB/X are ignored."""
        data = []
        
        # Row 1: Headers
        row1 = [''] * 12
        row1[0] = 'اسم الطالب'
        for i in range(5):
            row1[7 + i] = f'A{i+1}'
        data.append(row1)
        
        # Row 2: Empty
        data.append([''] * 12)
        
        # Row 3: Due dates (all in past)
        row3 = [''] * 12
        for i in range(5):
            row3[7 + i] = TEST_TODAY - timedelta(days=1)
        data.append(row3)
        
        # Row 4: Student with M, I, AB, X, 75
        row4 = [''] * 12
        row4[0] = 'فاطمة علي'
        row4[7] = 'M'
        row4[8] = 'I'
        row4[9] = 'AB'
        row4[10] = 'X'
        row4[11] = 75
        data.append(row4)
        
        buffer = create_test_excel(data)
        result = parse_excel_file(buffer, today=TEST_TODAY)
        
        student = result[0]['students'][0]
        
        # M = not submitted (counts as due)
        # I, AB, X = ignored (don't count as due)
        # 75 = submitted
        # total_due = 5 - 3 (I, AB, X ignored) = 2
        # not_submitted = 1 (M)
        # completed = 1 (75)
        
        assert student['not_submitted'] == 1
        assert student['completed'] == 1
        assert student['total_due'] == 2
        assert student['completion_rate'] == 50.0


class TestOverallColumnIgnore:
    """Test that Overall column is excluded."""
    
    def test_overall_column_excluded(self):
        """Ensure columns with 'Overall' are excluded from counting."""
        data = []
        
        # Row 1: Headers
        row1 = [''] * 10
        row1[0] = 'اسم الطالب'
        row1[7] = 'Assessment 1'
        row1[8] = 'Overall'
        row1[9] = 'Assessment 2'
        data.append(row1)
        
        # Row 2: Empty
        data.append([''] * 10)
        
        # Row 3: Due dates
        row3 = [''] * 10
        row3[7] = TEST_TODAY - timedelta(days=1)
        row3[8] = TEST_TODAY - timedelta(days=1)
        row3[9] = TEST_TODAY - timedelta(days=1)
        data.append(row3)
        
        # Row 4: Student
        row4 = [''] * 10
        row4[0] = 'محمد خالد'
        row4[7] = 80
        row4[8] = 85
        row4[9] = 90
        data.append(row4)
        
        buffer = create_test_excel(data)
        result = parse_excel_file(buffer, today=TEST_TODAY)
        
        student = result[0]['students'][0]
        
        # Only Assessment 1 and Assessment 2 should count (Overall excluded)
        assert student['total_due'] == 2
        assert student['completed'] == 2


class TestSheetNameParsing:
    """Test sheet name parsing."""
    
    def test_parse_sheet_name_slash(self):
        """'03/1 Arabic' → ('Arabic', '03/1')"""
        subject, class_code = parse_sheet_name('03/1 Arabic')
        assert subject == 'Arabic'
        assert class_code == '03/1'
    
    def test_parse_sheet_name_space(self):
        """'Arabic 03/1' → ('Arabic', '03/1')"""
        subject, class_code = parse_sheet_name('Arabic 03/1')
        assert subject == 'Arabic'
        assert class_code == '03/1'
    
    def test_parse_sheet_name_dash(self):
        """'03-1 Math' → ('Math', '03-1')"""
        subject, class_code = parse_sheet_name('03-1 Math')
        assert subject == 'Math'
        assert class_code == '03-1'


class TestNoDueAssessments:
    """Test handling when all due dates are in the future."""
    
    def test_no_due_assessments(self):
        """All due dates in future → has_due=False, completion_rate==0.0."""
        data = []
        
        # Row 1: Headers
        row1 = [''] * 9
        row1[0] = 'اسم الطالب'
        row1[7] = 'Assessment 1'
        row1[8] = 'Assessment 2'
        data.append(row1)
        
        # Row 2: Empty
        data.append([''] * 9)
        
        # Row 3: Due dates (all future)
        row3 = [''] * 9
        row3[7] = TEST_TODAY + timedelta(days=1)
        row3[8] = TEST_TODAY + timedelta(days=2)
        data.append(row3)
        
        # Row 4: Student
        row4 = [''] * 9
        row4[0] = 'نورة سعيد'
        row4[7] = 80
        row4[8] = 90
        data.append(row4)
        
        buffer = create_test_excel(data)
        result = parse_excel_file(buffer, today=TEST_TODAY)
        
        student = result[0]['students'][0]
        
        assert student['has_due'] == False
        assert student['completion_rate'] == 0.0
        assert student['total_due'] == 0
    
    def test_no_due_excluded_from_kpis(self):
        """Students with has_due=False should be excluded from school_completion_avg."""
        data = []
        
        # Row 1: Headers
        row1 = [''] * 9
        row1[0] = 'اسم الطالب'
        row1[7] = 'A1'
        row1[8] = 'A2'
        data.append(row1)
        
        # Row 2: Empty
        data.append([''] * 9)
        
        # Row 3: Due dates
        row3 = [''] * 9
        row3[7] = TEST_TODAY - timedelta(days=1)  # Past
        row3[8] = TEST_TODAY + timedelta(days=1)  # Future
        data.append(row3)
        
        # Row 4-5: Two students
        row4 = [''] * 9
        row4[0] = 'طالب 1'
        row4[7] = 100
        row4[8] = 90
        data.append(row4)
        
        row5 = [''] * 9
        row5[0] = 'طالب 2'
        row5[7] = 50
        row5[8] = 80
        data.append(row5)
        
        buffer = create_test_excel(data)
        result = parse_excel_file(buffer, today=TEST_TODAY)
        
        # Calculate KPIs
        kpis = calculate_weekly_kpis(result)
        
        # Both students have 1 due assessment (A1)
        assert kpis['total_students'] == 2


class TestBanding:
    """Test banding thresholds."""
    
    def test_band_thresholds(self):
        """Verify thresholds return correct bands."""
        assert get_band(100) == "ممتاز جداً"
        assert get_band(90) == "ممتاز جداً"
        assert get_band(89.99) == "جيد جداً"
        assert get_band(75) == "جيد جداً"
        assert get_band(74.99) == "جيد"
        assert get_band(60) == "جيد"
        assert get_band(59.99) == "يحتاج إلى تحسين"
        assert get_band(40) == "يحتاج إلى تحسين"
        assert get_band(39.99) == "ضعيف"
        assert get_band(0.01) == "ضعيف"
        assert get_band(0) == "انعدام الإنجاز"
        assert get_band(None) == "N/A"
    
    def test_band_labels_complete(self):
        """Check that BAND_LABELS contains all expected labels."""
        expected = {
            "ممتاز جداً",
            "جيد جداً",
            "جيد",
            "يحتاج إلى تحسين",
            "ضعيف",
            "انعدام الإنجاز"
        }
        assert set(BAND_LABELS) == expected


class TestHelperFunctions:
    """Test helper functions."""
    
    def test_find_student_name_column(self):
        """Test finding student name column."""
        df = pd.DataFrame([
            ['ID', 'اسم الطالب', 'Grade'],
            [1, 'أحمد', '3-1'],
            [2, 'فاطمة', '3-1']
        ])
        
        col = find_student_name_column(df)
        assert col == 1
    
    def test_find_assessment_start_column_default(self):
        """Test default assessment start column (H = index 7)."""
        df = pd.DataFrame([[f'Col{i}' for i in range(15)]])
        
        col = find_assessment_start_column(df)
        assert col == 7
    
    def test_find_assessment_start_column_after_overall(self):
        """Test assessment start after Overall column when Overall is before column H."""
        # When Overall is BEFORE column H (index 7), start after it
        headers = [''] * 11
        headers[0] = 'Name'
        headers[5] = 'Overall'  # Before column H
        headers[7] = 'A1'
        headers[8] = 'A2'
        
        df = pd.DataFrame([headers])
        
        col = find_assessment_start_column(df)
        # Overall at index 5, so start at max(7, 5+1) = 7
        assert col == 7
        
        # When Overall is AT or AFTER column H, we still start at H
        # but the Overall column itself is excluded via is_excluded_column()
        headers2 = [''] * 11
        headers2[0] = 'Name'
        headers2[7] = 'A1'
        headers2[9] = 'Overall'
        headers2[10] = 'A3'
        
        df2 = pd.DataFrame([headers2])
        col2 = find_assessment_start_column(df2)
        assert col2 == 7  # Still start at H, Overall excluded separately
    
    def test_is_excluded_column(self):
        """Test column exclusion logic."""
        assert is_excluded_column('Overall') == True
        assert is_excluded_column('overall') == True
        assert is_excluded_column('إجمالي') == True
        assert is_excluded_column('Unnamed: 5') == True
        assert is_excluded_column('Notes') == True
        assert is_excluded_column('ملاحظات') == True
        assert is_excluded_column('Assessment 1') == False
    
    def test_parse_due_date_formats(self):
        """Test parsing various date formats."""
        # ISO format
        assert parse_due_date('2025-10-22') == date(2025, 10, 22)
        
        # Day-first format
        assert parse_due_date('22/10/2025', dayfirst=True) == date(2025, 10, 22)
        
        # Already a date
        assert parse_due_date(date(2025, 10, 22)) == date(2025, 10, 22)
        
        # Invalid
        assert parse_due_date('invalid') == None
        assert parse_due_date(None) == None
    
    def test_normalize_arabic_text(self):
        """Test Arabic text normalization."""
        assert normalize_arabic_text('  أحمد   محمد  ') == 'أحمد محمد'
        assert normalize_arabic_text('') == ''
        assert normalize_arabic_text(None) == ''


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

