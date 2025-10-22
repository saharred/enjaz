"""
Tab 6 content for School Report with comprehensive analytical layout.
"""

import streamlit as st
import pandas as pd
import tempfile
import os

from enjaz.comprehensive_report_horizontal import (
    create_horizontal_comprehensive_report
)
from enjaz.comprehensive_report import (
    export_comprehensive_report_to_excel
)
from enjaz.analysis import get_band


def render_school_report_tab(all_data):
    """Render the school report tab with comprehensive analytical layout."""
    
    st.header("🏫 تقرير المدرسة - عرض أفقي شامل")
    
    st.info("""
    📌 **تقرير المدرسة الشامل**
    
    يعرض هذا التقرير جميع الطلاب مع تفاصيل أدائهم في جميع المواد بشكل أفقي:
    - اسم الطالب | المستوى | الشعبة
    - لكل مادة: إجمالي التقييمات | المنجز | نسبة الحل
    - النسبة الكلية للإنجاز | الفئة | التوصية
    """)
    
    try:
        # Create horizontal comprehensive report
        df = create_horizontal_comprehensive_report(all_data)
        
        if df.empty:
            st.warning("⚠️ لا توجد بيانات للعرض")
            return
        
        # Display summary metrics
        st.subheader("📊 ملخص التقرير")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate unique students
        unique_students = df['اسم الطالب'].nunique()
        
        # Calculate average completion
        avg_completion = df['نسبة الحل (%)'].mean()
        
        # Count subjects (from column names)
        subject_cols = [col for col in df.columns if ' - إجمالي' in col]
        unique_subjects = len(subject_cols)
        
        # Get overall band
        overall_band = get_band(avg_completion)
        
        with col1:
            st.metric("👥 إجمالي الطلاب", unique_students)
        
        with col2:
            st.metric("📚 عدد المواد", unique_subjects)
        
        with col3:
            st.metric("🎯 متوسط الإنجاز", f"{avg_completion:.1f}%")
        
        with col4:
            st.metric("🏆 الفئة العامة", overall_band)
        
        # Display the comprehensive report
        st.subheader("📋 التقرير التحليلي الشامل")
        
        st.dataframe(
            df,
            use_container_width=True,
            height=600
        )
        
        # Export options
        st.subheader("📥 تصدير التقرير")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export to Excel
            if st.button("📄 تصدير إلى Excel"):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                        excel_path = export_comprehensive_report_to_excel(
                            df,
                            tmp.name
                        )
                        
                        with open(excel_path, 'rb') as f:
                            excel_data = f.read()
                        
                        st.download_button(
                            label="⬇️ تحميل ملف Excel",
                            data=excel_data,
                            file_name="التقرير_التحليلي_الشامل.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        
                        # Clean up temp file
                        os.unlink(excel_path)
                        
                        st.success("✅ تم إنشاء ملف Excel بنجاح!")
                except Exception as e:
                    st.error(f"❌ حدث خطأ: {str(e)}")
        
        with col2:
            # Export to CSV
            if st.button("📊 تصدير إلى CSV"):
                try:
                    csv_data = df.to_csv(index=False, encoding='utf-8-sig')
                    
                    st.download_button(
                        label="⬇️ تحميل ملف CSV",
                        data=csv_data,
                        file_name="التقرير_التحليلي_الشامل.csv",
                        mime="text/csv"
                    )
                    
                    st.success("✅ تم إنشاء ملف CSV بنجاح!")
                except Exception as e:
                    st.error(f"❌ حدث خطأ: {str(e)}")
    
    except Exception as e:
        st.error(f"❌ حدث خطأ في إنشاء التقرير: {str(e)}")
        st.info("📊 البيانات متوفرة في التبويبات الأخرى")

