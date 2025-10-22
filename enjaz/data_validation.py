"""
Data validation module for Enjaz application.
Validates uploaded Excel files and data integrity.
"""

import pandas as pd
import streamlit as st


def validate_data(df, sheet_name="Sheet1"):
    """
    Validate uploaded DataFrame for required structure and data types.
    
    Args:
        df: pandas DataFrame to validate
        sheet_name: Name of the sheet being validated
    
    Returns:
        tuple: (is_valid: bool, error_messages: list)
    """
    errors = []
    
    # Check if DataFrame is empty
    if df.empty:
        errors.append("⚠️ الملف فارغ أو لا يحتوي على بيانات")
        return False, errors
    
    # Required columns (flexible - check for common LMS export columns)
    # The actual validation is flexible based on the LMS export format
    required_cols_patterns = [
        ['اسم', 'name', 'student'],  # Student name
        ['صف', 'grade', 'level'],     # Grade
    ]
    
    # Check for at least some recognizable columns
    df_cols_lower = [str(col).lower() for col in df.columns]
    
    found_patterns = 0
    for pattern_group in required_cols_patterns:
        for pattern in pattern_group:
            if any(pattern in col for col in df_cols_lower):
                found_patterns += 1
                break
    
    if found_patterns < 1:
        errors.append("""
        ⚠️ **تنسيق الملف غير صحيح**
        
        الملف لا يحتوي على الأعمدة المطلوبة. يرجى التأكد من:
        - الملف مصدّر من نظام LMS
        - يحتوي على معلومات الطلاب والتقييمات
        - أسماء الأعمدة واضحة ومفهومة
        """)
        return False, errors
    
    # Check for minimum number of rows
    if len(df) < 1:
        errors.append("⚠️ الملف يجب أن يحتوي على صف واحد على الأقل من البيانات")
        return False, errors
    
    # Check for excessive missing values
    missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    if missing_pct > 50:
        errors.append(f"⚠️ الملف يحتوي على نسبة عالية من القيم المفقودة ({missing_pct:.1f}%)")
    
    # If we have errors, return False
    if errors:
        return False, errors
    
    return True, []


def validate_uploaded_files(uploaded_files):
    """
    Validate multiple uploaded files.
    
    Args:
        uploaded_files: List of uploaded file objects from st.file_uploader
    
    Returns:
        tuple: (all_valid: bool, validation_results: dict)
    """
    if not uploaded_files:
        return False, {"error": "لم يتم رفع أي ملفات"}
    
    validation_results = {}
    all_valid = True
    
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        
        try:
            # Try to read the Excel file
            try:
                xl_file = pd.ExcelFile(uploaded_file)
                sheets = xl_file.sheet_names
                
                file_results = {
                    "status": "success",
                    "sheets": {},
                    "total_sheets": len(sheets)
                }
                
                # Validate each sheet
                for sheet_name in sheets:
                    try:
                        df = pd.read_excel(xl_file, sheet_name=sheet_name)
                        is_valid, errors = validate_data(df, sheet_name)
                        
                        file_results["sheets"][sheet_name] = {
                            "valid": is_valid,
                            "errors": errors,
                            "rows": len(df),
                            "columns": len(df.columns)
                        }
                        
                        if not is_valid:
                            all_valid = False
                            
                    except Exception as e:
                        file_results["sheets"][sheet_name] = {
                            "valid": False,
                            "errors": [f"خطأ في قراءة الورقة: {str(e)}"],
                            "rows": 0,
                            "columns": 0
                        }
                        all_valid = False
                
                validation_results[file_name] = file_results
                
            except Exception as e:
                validation_results[file_name] = {
                    "status": "error",
                    "error": f"خطأ في قراءة الملف: {str(e)}"
                }
                all_valid = False
                
        except Exception as e:
            validation_results[file_name] = {
                "status": "error",
                "error": f"خطأ غير متوقع: {str(e)}"
            }
            all_valid = False
    
    return all_valid, validation_results


def display_validation_results(validation_results):
    """
    Display validation results in Streamlit UI.
    
    Args:
        validation_results: Dictionary of validation results
    """
    for file_name, results in validation_results.items():
        with st.expander(f"📄 {file_name}", expanded=True):
            if results.get("status") == "error":
                st.error(f"❌ {results.get('error')}")
            else:
                st.success(f"✅ تم قراءة الملف بنجاح ({results.get('total_sheets')} ورقة)")
                
                for sheet_name, sheet_results in results.get("sheets", {}).items():
                    if sheet_results["valid"]:
                        st.info(f"✅ **{sheet_name}**: {sheet_results['rows']} صف، {sheet_results['columns']} عمود")
                    else:
                        st.warning(f"⚠️ **{sheet_name}**: مشاكل في البيانات")
                        for error in sheet_results.get("errors", []):
                            st.markdown(error)

