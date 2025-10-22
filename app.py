"""
Enjaz - Qatar Education Assessment Analysis System
Main Streamlit Application

Developed by: Sahar Osman (E-Projects Coordinator)
Email: Sahar.Osman@education.qa
School: Othman Bin Affan Model School for Boys
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Import Enjaz modules
from enjaz.ui import (
    apply_rtl_styling, 
    render_header, 
    render_footer, 
    show_welcome_screen,
    create_sidebar,
    render_metric_card,
    render_band_badge,
    QATAR_MAROON,
    QATAR_GOLD
)
from enjaz.data_ingest import aggregate_multiple_files
from enjaz.analysis import (
    calculate_weekly_kpis,
    calculate_class_stats,
    calculate_student_overall_stats,
    create_dataframe_for_class,
    get_band,
    get_band_color
)
from enjaz.recommendations import (
    get_recommendation_for_band,
    get_class_recommendations,
    generate_student_profile_recommendations
)
from enjaz.reports import (
    create_class_report_excel,
    create_overall_report_excel
)


# Page configuration
st.set_page_config(
    page_title="إنجاز - نظام تحليل التقييمات",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main application function."""
    
    # Apply RTL styling
    apply_rtl_styling()
    
    # Render header
    render_header()
    
    # Create sidebar and get user inputs
    uploaded_files, selected_view = create_sidebar()
    
    # Check if files are uploaded
    if not uploaded_files:
        show_welcome_screen()
        render_footer()
        return
    
    # Process uploaded files
    with st.spinner("جاري معالجة الملفات..."):
        all_data = aggregate_multiple_files(uploaded_files)
    
    if not all_data:
        st.error("❌ لم يتم العثور على بيانات صالحة في الملفات المرفوعة.")
        render_footer()
        return
    
    # Calculate statistics
    weekly_kpis = calculate_weekly_kpis(all_data)
    student_stats = calculate_student_overall_stats(all_data)
    
    # Store in session state
    st.session_state['all_data'] = all_data
    st.session_state['weekly_kpis'] = weekly_kpis
    st.session_state['student_stats'] = student_stats
    
    # Display selected view
    if selected_view == "لوحة المعلومات":
        show_dashboard(weekly_kpis, all_data)
    
    elif selected_view == "تقرير الصف/المادة":
        show_class_report(all_data)
    
    elif selected_view == "ملف الطالب":
        show_student_profile(all_data, student_stats)
    
    elif selected_view == "التقارير والتصدير":
        show_export_options(all_data, student_stats)
    
    # Render footer
    render_footer()


def show_dashboard(weekly_kpis, all_data):
    """Display dashboard with weekly KPIs and charts."""
    
    st.markdown("## 📊 لوحة المعلومات الأسبوعية")
    
    # KPI metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card(
            "إجمالي الطلاب",
            f"{weekly_kpis['total_students']}",
            "عدد الطلاب الفريد"
        )
    
    with col2:
        render_metric_card(
            "إجمالي التقييمات",
            f"{weekly_kpis['total_assessments']}",
            "عدد التقييمات المُحلّلة"
        )
    
    with col3:
        avg = weekly_kpis['overall_average']
        render_metric_card(
            "متوسط الإكمال",
            f"{avg:.1f}%",
            "المتوسط العام"
        )
    
    with col4:
        overall_band = get_band(weekly_kpis['overall_average'])
        badge_html = render_band_badge(overall_band)
        st.markdown(f"""
            <div class="metric-card">
                <h3>التصنيف العام</h3>
                <div style="margin-top: 1rem;">{badge_html}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Band distribution chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 توزيع الفئات")
        
        band_dist = weekly_kpis['band_distribution']
        if band_dist:
            # Translate band names to Arabic
            band_arabic = {
                "Platinum": "بلاتينيوم",
                "Gold": "ذهبي",
                "Silver": "فضي",
                "Bronze": "برونزي",
                "Needs Improvement": "يحتاج إلى تحسين"
            }
            
            labels = [band_arabic.get(k, k) for k in band_dist.keys()]
            values = list(band_dist.values())
            colors = [get_band_color(k) for k in band_dist.keys()]
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                marker=dict(colors=colors),
                textinfo='label+percent+value',
                textfont=dict(size=14)
            )])
            
            fig.update_layout(
                height=400,
                showlegend=True,
                font=dict(family="Cairo", size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📚 أفضل وأضعف المواد")
        
        st.markdown("#### 🏆 أفضل 5 مواد")
        for idx, subject in enumerate(weekly_kpis['top_subjects'][:5], 1):
            st.markdown(f"{idx}. **{subject['subject']}**: {subject['average']:.1f}%")
        
        st.markdown("#### ⚠️ أضعف 5 مواد")
        for idx, subject in enumerate(weekly_kpis['bottom_subjects'][:5], 1):
            st.markdown(f"{idx}. **{subject['subject']}**: {subject['average']:.1f}%")
    
    st.markdown("---")
    
    # Subject-wise performance table
    st.markdown("### 📋 أداء المواد التفصيلي")
    
    subject_data = []
    for sheet_data in all_data:
        class_stats = calculate_class_stats(sheet_data)
        if class_stats['average_completion'] is not None:
            subject_data.append({
                'المادة/الصف': sheet_data['sheet_name'],
                'عدد الطلاب': class_stats['valid_students'],
                'متوسط الإكمال': f"{class_stats['average_completion']:.1f}%",
                'التصنيف': get_band(class_stats['average_completion'])
            })
    
    if subject_data:
        df_subjects = pd.DataFrame(subject_data)
        st.dataframe(df_subjects, use_container_width=True, hide_index=True)


def show_class_report(all_data):
    """Display class/subject report with student details."""
    
    st.markdown("## 📚 تقرير الصف/المادة")
    
    # Select subject/class
    subject_names = [sheet['sheet_name'] for sheet in all_data]
    selected_subject = st.selectbox("اختر المادة/الصف", subject_names)
    
    # Find selected sheet data
    sheet_data = next((s for s in all_data if s['sheet_name'] == selected_subject), None)
    
    if not sheet_data:
        st.error("لم يتم العثور على البيانات المحددة.")
        return
    
    # Calculate class statistics
    class_stats = calculate_class_stats(sheet_data)
    
    # Display class metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_metric_card(
            "إجمالي الطلاب",
            f"{class_stats['total_students']}",
            f"طلاب صالحون: {class_stats['valid_students']}"
        )
    
    with col2:
        avg = class_stats['average_completion']
        if avg is not None:
            render_metric_card(
                "متوسط الإكمال",
                f"{avg:.1f}%",
                get_band(avg)
            )
    
    with col3:
        st.markdown("### 📊 توزيع الفئات")
        for band, count in class_stats['band_distribution'].items():
            badge = render_band_badge(band)
            st.markdown(f"{badge} {count} طالب/طلاب", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Student table
    st.markdown("### 📋 قائمة الطلاب")
    
    df_class = create_dataframe_for_class(sheet_data)
    st.dataframe(df_class, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Class recommendations
    st.markdown("### 💡 التوصيات")
    
    recommendations = get_class_recommendations(class_stats, selected_subject)
    st.markdown(recommendations)
    
    st.markdown("---")
    
    # Top performers and needs attention
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌟 الطلاب المتميزون")
        for student in class_stats['top_performers'][:5]:
            badge = render_band_badge(get_band(student['completion_rate']))
            st.markdown(
                f"**{student['student_name']}**: {student['completion_rate']:.1f}% {badge}",
                unsafe_allow_html=True
            )
    
    with col2:
        st.markdown("### ⚠️ الطلاب الذين يحتاجون إلى اهتمام")
        for student in class_stats['needs_attention'][:5]:
            badge = render_band_badge(get_band(student['completion_rate']))
            st.markdown(
                f"**{student['student_name']}**: {student['completion_rate']:.1f}% {badge}",
                unsafe_allow_html=True
            )


def show_student_profile(all_data, student_stats):
    """Display individual student profile."""
    
    st.markdown("## 👤 ملف الطالب")
    
    # Select student
    student_names = sorted(student_stats.keys())
    selected_student = st.selectbox("اختر الطالب", student_names)
    
    if not selected_student:
        st.info("الرجاء اختيار طالب لعرض ملفه.")
        return
    
    student_data = student_stats[selected_student]
    
    # Display student metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_metric_card(
            "إجمالي المكتمل",
            f"{student_data['total_completed']}",
            f"من أصل {student_data['total_assigned']}"
        )
    
    with col2:
        rate = student_data['overall_completion_rate']
        if rate is not None:
            render_metric_card(
                "نسبة الإكمال",
                f"{rate:.1f}%",
                "المعدل الإجمالي"
            )
    
    with col3:
        badge = render_band_badge(student_data['overall_band'])
        st.markdown(f"""
            <div class="metric-card">
                <h3>التصنيف الإجمالي</h3>
                <div style="margin-top: 1rem; font-size: 1.5rem;">{badge}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Subject performance chart
    st.markdown("### 📊 الأداء حسب المادة")
    
    subjects = student_data.get('subjects', [])
    if subjects:
        subject_names = [s['subject'] for s in subjects]
        completion_rates = [s['completion_rate'] for s in subjects]
        colors_list = [get_band_color(s['band']) for s in subjects]
        
        fig = go.Figure(data=[
            go.Bar(
                x=completion_rates,
                y=subject_names,
                orientation='h',
                marker=dict(color=colors_list),
                text=[f"{rate:.1f}%" for rate in completion_rates],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            xaxis_title="نسبة الإكمال (%)",
            yaxis_title="المادة",
            height=400,
            font=dict(family="Cairo", size=12),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Subject details table
    st.markdown("### 📋 تفاصيل المواد")
    
    if subjects:
        subject_table_data = []
        for s in subjects:
            subject_table_data.append({
                'المادة': s['subject'],
                'نسبة الإكمال': f"{s['completion_rate']:.1f}%",
                'التصنيف': s['band']
            })
        
        df_subjects = pd.DataFrame(subject_table_data)
        st.dataframe(df_subjects, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Student recommendations
    st.markdown("### 💡 التوصيات")
    
    recommendations = generate_student_profile_recommendations(student_data)
    st.markdown(recommendations)


def show_export_options(all_data, student_stats):
    """Display export options for reports."""
    
    st.markdown("## 📥 التقارير والتصدير")
    
    st.markdown("""
        يمكنك تصدير التقارير بصيغة Excel للاستخدام والمشاركة.
    """)
    
    st.markdown("---")
    
    # Export overall report
    st.markdown("### 📊 التقرير الإجمالي")
    st.markdown("تقرير شامل لجميع الطلاب مع التصنيفات الإجمالية.")
    
    if st.button("تصدير التقرير الإجمالي (Excel)"):
        with st.spinner("جاري إنشاء التقرير..."):
            excel_buffer = create_overall_report_excel(all_data, student_stats)
            
            st.download_button(
                label="📥 تحميل التقرير الإجمالي",
                data=excel_buffer,
                file_name=f"overall_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    st.markdown("---")
    
    # Export class reports
    st.markdown("### 📚 تقارير المواد/الصفوف")
    st.markdown("تقارير تفصيلية لكل مادة/صف على حدة.")
    
    subject_names = [sheet['sheet_name'] for sheet in all_data]
    selected_subject_export = st.selectbox("اختر المادة/الصف للتصدير", subject_names, key="export_subject")
    
    if st.button("تصدير تقرير المادة (Excel)"):
        sheet_data = next((s for s in all_data if s['sheet_name'] == selected_subject_export), None)
        
        if sheet_data:
            with st.spinner("جاري إنشاء التقرير..."):
                class_stats = calculate_class_stats(sheet_data)
                excel_buffer = create_class_report_excel(sheet_data, class_stats)
                
                safe_filename = selected_subject_export.replace('/', '_').replace('\\', '_')
                
                st.download_button(
                    label=f"📥 تحميل تقرير {selected_subject_export}",
                    data=excel_buffer,
                    file_name=f"{safe_filename}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )


if __name__ == "__main__":
    main()

