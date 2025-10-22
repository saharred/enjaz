"""
Tab 7 content for Analytics Export with detailed student-subject breakdown.
"""

import streamlit as st
import pandas as pd
import tempfile
import os

from enjaz.analytics_export import (
    create_analytics_export,
    export_analytics_to_excel,
    export_analytics_to_csv
)
from enjaz.analysis import get_band


def render_analytics_export_tab(all_data):
    """Render the analytics export tab with detailed student-subject breakdown."""
    
    st.header("📊 التصدير التحليلي - Analytics Export")
    
    st.info("""
    📌 **التصدير التحليلي الشامل**
    
    يعرض هذا التقرير صف واحد لكل طالب × مادة مع النسبة العامة عبر جميع المواد:
    - اسم الطالب | الصف | الشعبة | المادة
    - إجمالي المادة | منجز في المادة
    - النسبة العامة لكل المواد | الفئة
    
    **مثالي للتحليل في Excel أو Python!**
    """)
    
    try:
        # Create analytics export
        df = create_analytics_export(all_data)
        
        if df.empty:
            st.warning("⚠️ لا توجد بيانات للعرض")
            return
        
        # Display summary metrics
        st.subheader("📊 ملخص التقرير")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate metrics
        unique_students = df['student_name'].nunique()
        unique_subjects = df['subject'].nunique()
        total_rows = len(df)
        avg_overall = df.groupby('student_name')['overall_pct_all_subjects'].first().mean()
        
        with col1:
            st.metric("👥 إجمالي الطلاب", unique_students)
        
        with col2:
            st.metric("📚 عدد المواد", unique_subjects)
        
        with col3:
            st.metric("📋 إجمالي الصفوف", total_rows)
        
        with col4:
            st.metric("🎯 متوسط النسبة العامة", f"{avg_overall:.1f}%")
        
        # Display tier distribution
        st.subheader("📈 توزيع الفئات")
        
        tier_counts = df.groupby('student_name')['tier'].first().value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(
                tier_counts.reset_index().rename(columns={'index': 'الفئة', 'tier': 'عدد الطلاب'}),
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            # Create a simple bar chart
            import plotly.express as px
            fig = px.bar(
                x=tier_counts.index,
                y=tier_counts.values,
                labels={'x': 'الفئة', 'y': 'عدد الطلاب'},
                title='توزيع الطلاب حسب الفئة'
            )
            fig.update_layout(
                xaxis_title='الفئة',
                yaxis_title='عدد الطلاب',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Display the analytics export
        st.subheader("📋 التقرير التحليلي الشامل")
        
        st.dataframe(
            df,
            use_container_width=True,
            height=600
        )
        
        # Column descriptions
        with st.expander("ℹ️ وصف الأعمدة"):
            st.markdown("""
            ### الأعمدة:
            
            1. **student_name** - اسم الطالب
            2. **grade** - الصف/المستوى الدراسي
            3. **section** - الشعبة/الفصل
            4. **subject** - المادة
            5. **subject_total_assigned** - إجمالي التقييمات المكلف بها في هذه المادة
            6. **subject_total_done** - عدد التقييمات المنجزة في هذه المادة
            7. **overall_pct_all_subjects** - النسبة العامة للإنجاز عبر **جميع المواد** (نفس القيمة لكل مواد الطالب)
            8. **tier** - الفئة حسب النسبة العامة
            
            ### معايير التصنيف:
            
            - **بلاتينية:** >= 90%
            - **ذهبية:** >= 80% و < 90%
            - **فضية:** >= 70% و < 80%
            - **برونزية:** >= 50% و < 70%
            - **يحتاج إلى تطوير:** >= 1% و < 50%
            - **لا يستفيد من النظام:** = 0%
            """)
        
        # Export options
        st.subheader("📥 تصدير التقرير")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export to Excel
            if st.button("📄 تصدير إلى Excel", use_container_width=True):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                        excel_path = export_analytics_to_excel(df, tmp.name)
                        
                        with open(excel_path, 'rb') as f:
                            excel_data = f.read()
                        
                        st.download_button(
                            label="⬇️ تحميل ملف Excel",
                            data=excel_data,
                            file_name="analytics_export_injaz.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                        
                        # Clean up
                        try:
                            os.unlink(excel_path)
                        except:
                            pass
                        
                        st.success("✅ تم إنشاء ملف Excel بنجاح!")
                
                except Exception as e:
                    st.error(f"❌ خطأ في التصدير إلى Excel: {str(e)}")
        
        with col2:
            # Export to CSV
            if st.button("📄 تصدير إلى CSV", use_container_width=True):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w', encoding='utf-8-sig') as tmp:
                        csv_path = export_analytics_to_csv(df, tmp.name)
                        
                        with open(csv_path, 'rb') as f:
                            csv_data = f.read()
                        
                        st.download_button(
                            label="⬇️ تحميل ملف CSV",
                            data=csv_data,
                            file_name="analytics_export_injaz.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                        
                        # Clean up
                        try:
                            os.unlink(csv_path)
                        except:
                            pass
                        
                        st.success("✅ تم إنشاء ملف CSV بنجاح!")
                
                except Exception as e:
                    st.error(f"❌ خطأ في التصدير إلى CSV: {str(e)}")
        
        # Sample code for analysis
        with st.expander("💻 كود Python للتحليل"):
            st.code("""
import pandas as pd

# قراءة الملف
df = pd.read_excel('analytics_export_injaz.xlsx')

# أو
df = pd.read_csv('analytics_export_injaz.csv')

# عرض أول 5 صفوف
print(df.head())

# إحصائيات عامة
print(df.describe())

# الطلاب في الفئة البلاتينية
platinum = df[df['tier'] == 'بلاتينية']['student_name'].unique()
print(f"الطلاب البلاتينيون: {platinum}")

# متوسط الإنجاز لكل مادة
subject_avg = df.groupby('subject').apply(
    lambda x: (x['subject_total_done'].sum() / x['subject_total_assigned'].sum() * 100)
)
print(subject_avg)

# الطلاب الذين يحتاجون إلى دعم (< 70%)
needs_support = df[df['overall_pct_all_subjects'] < 70]['student_name'].unique()
print(f"يحتاجون إلى دعم: {needs_support}")
            """, language='python')
    
    except Exception as e:
        st.error(f"❌ حدث خطأ: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

