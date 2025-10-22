"""
Tab 6 content for School Report with comprehensive analytical layout.
"""

import streamlit as st
import pandas as pd
import tempfile
import os

from enjaz.comprehensive_report import (
    create_comprehensive_report,
    export_comprehensive_report_to_excel,
    export_comprehensive_report_to_word
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
        # Create comprehensive report
        df = create_comprehensive_report(all_data)
        
        if df.empty:
            st.warning("⚠️ لا توجد بيانات للعرض")
            return
        
        # Display summary metrics
        st.subheader("📊 ملخص التقرير")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate unique students
        unique_students = df['اسم الطالب'].nunique()
        
        # Calculate average completion
        avg_completion = df.groupby('اسم الطالب')['النسبة الكلية للإنجاز (%)'].first().mean()
        
        # Count subjects
        unique_subjects = df['المادة'].nunique()
        
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
        
        col1, col2, col3 = st.columns(3)
        
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
            # Export to Word
            if st.button("📝 تصدير إلى Word"):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
                        word_path = export_comprehensive_report_to_word(
                            df,
                            tmp.name
                        )
                        
                        with open(word_path, 'rb') as f:
                            word_data = f.read()
                        
                        st.download_button(
                            label="⬇️ تحميل ملف Word",
                            data=word_data,
                            file_name="التقرير_التحليلي_الشامل.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                        
                        # Clean up temp file
                        os.unlink(word_path)
                        
                        st.success("✅ تم إنشاء ملف Word بنجاح!")
                except Exception as e:
                    st.error(f"❌ حدث خطأ: {str(e)}")
        
        with col3:
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

