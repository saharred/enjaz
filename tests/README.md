# 🧪 Enjaz Test Suite

## Overview

This directory contains automated tests for the Enjaz assessment analysis system using pytest.

## Test Coverage

### Data Ingestion (`test_ingest_analysis.py`)

#### ✅ Due Date Filtering
- Tests that only assessments with `due_date <= today` are counted
- Verifies future assessments are excluded from calculations

#### ✅ Special Value Handling (M/I/AB/X)
- **M**: Counted as "not submitted"
- **I, AB, X**: Ignored (not counted in total_due)
- **Numeric values**: Counted as submitted

#### ✅ Overall Column Exclusion
- Ensures columns with "Overall" in the header are excluded
- Tests both before and after column H scenarios

#### ✅ Sheet Name Parsing
- `'03/1 Arabic'` → `('Arabic', '03/1')`
- `'Arabic 03/1'` → `('Arabic', '03/1')`
- `'03-1 Math'` → `('Math', '03-1')`

#### ✅ No Due Assessments
- Students with all future assessments: `has_due=False`, `completion_rate=0.0`
- Such students are excluded from school-wide KPIs

#### ✅ Banding Thresholds
- 90-100%: ممتاز جداً
- 75-89.99%: جيد جداً
- 60-74.99%: جيد
- 40-59.99%: يحتاج إلى تحسين
- 0.01-39.99%: ضعيف
- 0%: انعدام الإنجاز

#### ✅ Helper Functions
- Student name column detection
- Assessment start column detection
- Column exclusion logic
- Date parsing (multiple formats)
- Arabic text normalization

## Running Tests

### Run All Tests

```bash
cd /path/to/enjaz
python3 -m pytest tests/ -v
```

### Run Specific Test File

```bash
python3 -m pytest tests/test_ingest_analysis.py -v
```

### Run Specific Test Class

```bash
python3 -m pytest tests/test_ingest_analysis.py::TestBanding -v
```

### Run Specific Test

```bash
python3 -m pytest tests/test_ingest_analysis.py::TestBanding::test_band_thresholds -v
```

### Run with Coverage

```bash
pip3 install pytest-cov
python3 -m pytest tests/ --cov=enjaz --cov-report=html
```

## Test Data

All tests use a deterministic date: **October 22, 2025**

This ensures consistent test results regardless of when tests are run.

## Test Results

Current status: **✅ 16/16 tests passing**

```
tests/test_ingest_analysis.py::TestDueDateFiltering::test_future_assessment_excluded PASSED
tests/test_ingest_analysis.py::TestSpecialValueHandling::test_m_i_ab_x_handling PASSED
tests/test_ingest_analysis.py::TestOverallColumnIgnore::test_overall_column_excluded PASSED
tests/test_ingest_analysis.py::TestSheetNameParsing::test_parse_sheet_name_slash PASSED
tests/test_ingest_analysis.py::TestSheetNameParsing::test_parse_sheet_name_space PASSED
tests/test_ingest_analysis.py::TestSheetNameParsing::test_parse_sheet_name_dash PASSED
tests/test_ingest_analysis.py::TestNoDueAssessments::test_no_due_assessments PASSED
tests/test_ingest_analysis.py::TestNoDueAssessments::test_no_due_excluded_from_kpis PASSED
tests/test_ingest_analysis.py::TestBanding::test_band_thresholds PASSED
tests/test_ingest_analysis.py::TestBanding::test_band_labels_complete PASSED
tests/test_ingest_analysis.py::TestHelperFunctions::test_find_student_name_column PASSED
tests/test_ingest_analysis.py::TestHelperFunctions::test_find_assessment_start_column_default PASSED
tests/test_ingest_analysis.py::TestHelperFunctions::test_find_assessment_start_column_after_overall PASSED
tests/test_ingest_analysis.py::TestHelperFunctions::test_is_excluded_column PASSED
tests/test_ingest_analysis.py::TestHelperFunctions::test_parse_due_date_formats PASSED
tests/test_ingest_analysis.py::TestHelperFunctions::test_normalize_arabic_text PASSED
```

## Adding New Tests

1. Create test functions starting with `test_`
2. Use descriptive names
3. Add docstrings explaining what is being tested
4. Use the `TEST_TODAY` constant for date comparisons
5. Use the `create_test_excel()` helper for creating test data

Example:

```python
def test_new_feature(self):
    """Test description here."""
    # Arrange
    data = create_test_data()
    
    # Act
    result = function_to_test(data)
    
    # Assert
    assert result == expected_value
```

## Continuous Integration

These tests can be integrated with GitHub Actions for automatic testing on every commit.

Example `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python -m pytest tests/ -v
```

## Best Practices

- ✅ Keep tests independent
- ✅ Use descriptive test names
- ✅ Test edge cases
- ✅ Use fixtures for common setup
- ✅ Keep tests fast
- ✅ One assertion per test (when possible)

---

**Developed by**: Sahar Osman  
**Email**: Sahar.Osman@education.qa  
**School**: Othman Bin Affan Model School for Boys

© 2025 — All Rights Reserved

