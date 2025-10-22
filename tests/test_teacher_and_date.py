"""
Additional tests for teacher directory and date filtering.
"""

import pytest
import pandas as pd
from datetime import date, timedelta
from io import BytesIO

from enjaz.teacher_directory import (
    load_teacher_directory,
    merge_teacher_directory,
    filter_by_teacher_emails,
    get_all_teacher_emails
)
from enjaz.date_filter import filter_by_date_range


# Test date
TEST_TODAY = date(2025, 10, 22)


class TestTeacherDirectory:
    """Test teacher directory functionality."""
    
    def test_teacher_directory_merge(self):
        """Two teachers teaching same subject → emails concatenated with '; '."""
        # Create teacher directory Excel file
        teacher_data = {
            'Teacher Name': ['Teacher 1', 'Teacher 2'],
            'Email': ['t1@sch.qa', 't2@sch.qa'],
            'Subject': ['Math', 'Math'],
            'Class': ['03/1', '03/1']
        }
        
        teacher_df = pd.DataFrame(teacher_data)
        
        # Save to Excel buffer
        buffer = BytesIO()
        teacher_df.to_excel(buffer, index=False)
        buffer.seek(0)
        
        # Load using load_teacher_directory
        teacher_df = load_teacher_directory(buffer)
        
        # Create assessment data
        all_data = [{
            'sheet_name': 'Math 03/1',
            'subject': 'Math',
            'class_code': '03/1',
            'students': []
        }]
        
        # Merge
        result = merge_teacher_directory(all_data, teacher_df)
        
        # Check emails are concatenated
        assert result[0]['teacher_emails'] == 't1@sch.qa; t2@sch.qa'
        assert result[0]['teacher_names'] == 'Teacher 1; Teacher 2'
    
    def test_email_filtering(self):
        """Filter data by teacher email."""
        # Create data with teacher emails
        all_data = [
            {
                'sheet_name': 'Math',
                'subject': 'Math',
                'teacher_emails': 't1@sch.qa',
                'students': []
            },
            {
                'sheet_name': 'Science',
                'subject': 'Science',
                'teacher_emails': 't2@sch.qa',
                'students': []
            },
            {
                'sheet_name': 'English',
                'subject': 'English',
                'teacher_emails': 't1@sch.qa; t2@sch.qa',
                'students': []
            }
        ]
        
        # Filter by t1@sch.qa
        filtered = filter_by_teacher_emails(all_data, ['t1@sch.qa'])
        
        # Should get Math and English
        assert len(filtered) == 2
        subjects = [d['subject'] for d in filtered]
        assert 'Math' in subjects
        assert 'English' in subjects
    
    def test_get_all_emails(self):
        """Get all unique teacher emails."""
        all_data = [
            {'teacher_emails': 't1@sch.qa'},
            {'teacher_emails': 't2@sch.qa'},
            {'teacher_emails': 't1@sch.qa; t3@sch.qa'}
        ]
        
        emails = get_all_teacher_emails(all_data)
        
        assert len(emails) == 3
        assert 't1@sch.qa' in emails
        assert 't2@sch.qa' in emails
        assert 't3@sch.qa' in emails


class TestDateFiltering:
    """Test date range filtering."""
    
    def test_date_range_filter(self):
        """Filter assessments by date range and recompute metrics."""
        # Create data with assessments on different dates
        all_data = [{
            'sheet_name': 'Test',
            'subject': 'Test',
            'students': [{
                'student_name': 'Student 1',
                'total_due': 3,
                'completed': 2,
                'not_submitted': 1,
                'completion_rate': 66.67,
                'has_due': True,
                'assessments': [
                    {'title': 'A1', 'due_date': date(2025, 10, 1), 'value': 100},
                    {'title': 'A2', 'due_date': date(2025, 10, 15), 'value': 80},
                    {'title': 'A3', 'due_date': date(2025, 10, 20), 'value': 'M'}
                ]
            }]
        }]
        
        # Filter to only October 15-20
        start_date = date(2025, 10, 15)
        end_date = date(2025, 10, 20)
        
        filtered = filter_by_date_range(all_data, start_date, end_date)
        
        student = filtered[0]['students'][0]
        
        # Should only count A2 and A3
        assert student['total_due'] == 2
        assert student['completed'] == 1  # A2
        assert student['not_submitted'] == 1  # A3
        assert student['completion_rate'] == 50.0
    
    def test_date_filter_no_start(self):
        """Filter with only end date."""
        all_data = [{
            'sheet_name': 'Test',
            'students': [{
                'student_name': 'Student 1',
                'assessments': [
                    {'title': 'A1', 'due_date': date(2025, 10, 1), 'value': 100},
                    {'title': 'A2', 'due_date': date(2025, 10, 25), 'value': 80}
                ]
            }]
        }]
        
        # Only end date
        end_date = date(2025, 10, 15)
        
        filtered = filter_by_date_range(all_data, end_date=end_date)
        
        student = filtered[0]['students'][0]
        
        # Should only count A1
        assert student['total_due'] == 1
        assert student['completed'] == 1


class TestStudentProfilePDF:
    """Test student profile PDF export."""
    
    def test_pdf_export_non_empty(self):
        """PDF export should write non-empty bytes."""
        from enjaz.student_profile_pdf import create_student_profile_pdf
        
        student_data = [
            {
                'subject': 'Math',
                'total_due': 10,
                'completed': 8,
                'completion_rate': 80.0,
                'band': 'جيد جداً'
            },
            {
                'subject': 'Science',
                'total_due': 8,
                'completed': 7,
                'completion_rate': 87.5,
                'band': 'جيد جداً'
            }
        ]
        
        pdf_buffer = create_student_profile_pdf(
            'أحمد محمد',
            student_data,
            'جيد جداً'
        )
        
        # Check PDF is not empty
        pdf_bytes = pdf_buffer.getvalue()
        assert len(pdf_bytes) > 0
        
        # Check PDF header
        assert pdf_bytes[:4] == b'%PDF'
    
    def test_pdf_contains_advisory_text(self):
        """PDF should contain fixed advisory lines."""
        from enjaz.student_profile_pdf import create_student_profile_pdf
        
        student_data = [{
            'subject': 'Math',
            'total_due': 10,
            'completed': 8,
            'completion_rate': 80.0,
            'band': 'جيد جداً'
        }]
        
        pdf_buffer = create_student_profile_pdf(
            'فاطمة علي',
            student_data,
            'جيد جداً'
        )
        
        # PDF should be generated successfully
        assert pdf_buffer.getvalue()[:4] == b'%PDF'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

