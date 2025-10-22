"""
Tab 6 content for School Report with horizontal layout.
"""

import streamlit as st
import pandas as pd
import tempfile
import os

from enjaz.school_report import (
    create_horizontal_school_report,
    create_filtered_school_report,
    export_school_report_to_excel,
    get_unique_grades,
    get_unique_sections,
    create_descriptive_report
)


def render_school_report_tab(all_data):
    """Render the school report tab with horizontal layout."""
    
    st.header("🏫 تقرير المدرسة - عرض أفقي شامل")
    
    st.info("""
    📌 **تقرير المدرسة الشامل**
    
    يعرض هذا التقرير جميع الطلاب مع تفاصيل أدائهم في جميع المواد بشكل أفقي:
    - اسم الطالب | المستوى | الشعبة
    - لكل مادة: إجمالي التقييمات | المنجز
    - نسبة الحل العامة | الفئة
    """)
    
    # Filters
    st.subheader("🔍 فلاتر التقرير")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Grade filter
        available_grades = get_unique_grades(all_data)
        
        if available_grades:
            selected_grades = st.multiselect(
                "📚 اختر المستوى (الصف)",
                options=available_grades,
                default=available_grades,
                help="اختر المستويات المراد عرضها في التقرير"
            )
        else:
            selected_grades = []
            st.warning("⚠️ لا توجد مستويات متاحة")
    
    with col2:
        # Section filter
        available_sections = get_unique_sections(all_data)
        
        if available_sections:
            selected_sections = st.multiselect(
                "🏛️ اختر الشعبة",
                options=available_sections,
                default=available_sections,
                help="اختر الشعب المراد عرضها في التقرير"
            )
        else:
            selected_sections = []
            st.warning("⚠️ لا توجد شعب متاحة")
    
    # Generate report
    if not selected_grades and not selected_sections:
        st.warning("⚠️ الرجاء اختيار مستوى أو شعبة واحدة على الأقل")
        return
    
    # Create filtered report
    if selected_grades or selected_sections:
        df = create_filtered_school_report(all_data, selected_grades, selected_sections)
    else:
        df = create_horizontal_school_report(all_data)
    
    if df.empty:
        st.error("❌ لا توجد بيانات متاحة للفلاتر المحددة")
        return
    
    # Display summary metrics
    st.subheader("📊 ملخص التقرير")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 إجمالي الطلاب", len(df))
    
    with col2:
        # Count subjects (columns ending with "- إجمالي")
        subject_cols = [col for col in df.columns if col.endswith(" - إجمالي")]
        st.metric("📚 عدد المواد", len(subject_cols))
    
    with col3:
        # Calculate average completion
        completion_rates = df['نسبة الحل العامة'].str.rstrip('%').astype(float)
        avg_completion = completion_rates.mean()
        st.metric("🎯 متوسط الإنجاز", f"{avg_completion:.1f}%")
    
    with col4:
        # Count students in excellent category
        excellent_count = df['الفئة'].str.contains('ممتاز جداً').sum()
        st.metric("⭐ ممتاز جداً", excellent_count)
    
    # Display the horizontal report
    st.subheader("📋 تقرير المدرسة الأفقي")
    
    st.dataframe(
        df,
        use_container_width=True,
        height=600
    )
    
    # Descriptive report
    st.subheader("📝 التقرير الوصفي")
    
    descriptive_report = create_descriptive_report(df)
    
    st.text_area(
        "التقرير الوصفي الإحصائي",
        value=descriptive_report,
        height=400,
        help="ملخص إحصائي وتوصيات بناءً على أداء المدرسة"
    )
    
    # Export options
    st.subheader("📥 تصدير التقرير")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export to Excel
        if st.button("📄 تصدير إلى Excel"):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                    excel_path = export_school_report_to_excel(
                        df,
                        tmp.name,
                        "مدرسة عثمان بن عفان"
                    )
                    
                    with open(excel_path, 'rb') as f:
                        excel_data = f.read()
                    
                    st.download_button(
                        label="⬇️ تحميل ملف Excel",
                        data=excel_data,
                        file_name="تقرير_المدرسة_الشامل.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                    # Clean up temp file
                    os.unlink(excel_path)
                    
                    st.success("✅ تم إنشاء ملف Excel بنجاح!")
            except Exception as e:
                st.error(f"❌ حدث خطأ: {str(e)}")
    
    with col2:
        # Export descriptive report
        if st.button("📧 نسخ التقرير الوصفي"):
            st.code(descriptive_report, language=None)
            st.success("✅ يمكنك نسخ التقرير الوصفي من الأعلى!")

