"""
Enjaz - نظام تحليل التقييمات الإلكترونية الأسبوعية
Main Streamlit Application with Advanced Features
"""

import streamlit as st
import pandas as pd
from datetime import date
import pytz
from pathlib import Path
import base64

# Import Enjaz modules
from enjaz.data_ingest_lms import aggregate_lms_files
from enjaz.analysis import calculate_weekly_kpis, calculate_class_stats, get_band
from enjaz.school_info import load_school_info, save_school_info
from enjaz.advanced_charts import (
    create_band_distribution_chart,
    create_class_comparison_chart,
    create_subject_comparison_chart,
    create_comprehensive_dashboard
)
from enjaz.individual_reports import (
    create_student_individual_report,
    create_class_subject_report
)
from enjaz.student_analysis import (
    create_student_analysis_table,
    create_student_summary_by_grade,
    create_student_summary_by_subject,
    create_student_summary_by_band,
    export_student_analysis_to_excel
)
from enjaz.school_report import (
    create_horizontal_school_report,
    create_filtered_school_report,
    export_school_report_to_excel,
    get_unique_grades,
    get_unique_sections,
    create_descriptive_report
)
from enjaz.professional_design import (
    get_professional_css,
    get_header_html,
    get_footer_html,
    get_metric_card_html,
    QATAR_MAROON,
    QATAR_GOLD
)
from tab7_analytics_export import render_analytics_export_tab

# Page configuration
st.set_page_config(
    page_title="إنجاز - نظام تحليل التقييمات | Injaz Assessment System",
    page_icon="enjaz/assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:Sahar.Osman@education.qa',
        'Report a bug': 'https://github.com/saharred/enjaz/issues',
        'About': '# إنجاز - Injaz\n\nنظام تحليل التقييمات الأسبوعية\n\nمدرسة عثمان بن عفّان النموذجية للبنين\n\nوزارة التعليم والتعليم العالي - دولة قطر 🇶🇦'
    }
)

# Qatar brand colors are now imported from professional_design


def get_base64_image(image_path):
    """Convert image to base64 for embedding in HTML."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None


def apply_professional_design():
    """Apply professional Flat Design CSS."""
    # Get and apply professional CSS
    css = get_professional_css()
    st.markdown(css, unsafe_allow_html=True)


def render_professional_header():
    """Render professional header with new logo."""
    assets_path = Path(__file__).parent / 'enjaz' / 'assets'
    logo_horizontal_path = assets_path / 'logo_horizontal.png'
    
    # Get base64 encoded logo
    logo_b64 = None
    if logo_horizontal_path.exists():
        logo_b64 = get_base64_image(logo_horizontal_path)
    
    # Create logo data URL
    logo_url = f"data:image/png;base64,{logo_b64}" if logo_b64 else None
    
    # Get header HTML
    header_html = get_header_html(logo_url)
    st.markdown(header_html, unsafe_allow_html=True)


def render_professional_footer():
    """Render professional footer."""
    footer_html = get_footer_html()
    st.markdown(footer_html, unsafe_allow_html=True)
    return
    
    # Old footer code (to be removed)
    old_footer_html = f"""
    <div class="custom-footer">
        <p style="margin:0;"><strong>© 2025 — جميع الحقوق محفوظة</strong></p>
        <p style="margin:0;"><strong>مدرسة عثمان بن عفّان النموذجية للبنين</strong></p>
        <p style="margin:5px 0; font-size:0.95rem;">تطوير و تنفيذ: <strong>Sahar Osman</strong></p>
        <p style="margin:0; font-size:0.9rem; font-style:italic;">E-learning Project Coordinator</p>
        <p style="margin:10px 0 0 0; color:{QATAR_GOLD}; font-weight:bold;">
            📧 <a href="mailto:S.mahgou0101@education.qa" style="color:{QATAR_GOLD}; text-decoration:none;">S.mahgou0101@education.qa</a>
        </p>
        <p style="margin:5px 0;">
            <a href="https://www.linkedin.com/in/sahar-osman-a19a45209/" target="_blank" style="text-decoration:none;">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" width="24" style="vertical-align:middle; margin-left:5px;"/>
                <span style="color:{QATAR_GOLD}; font-weight:bold;">LinkedIn</span>
            </a>
        </p>
        <p style="margin-top:15px; font-style:italic; border-top:1px solid rgba(255,255,255,0.2); padding-top:10px;">رؤيتنا: "متعلم ريادي لتنمية مستدامة"</p>
    </div>
    """
    
    st.markdown(footer_html, unsafe_allow_html=True)


def school_info_settings():
    """Sidebar section for school information settings."""
    with st.sidebar.expander("⚙️ إعدادات المدرسة", expanded=False):
        school_info = load_school_info()
        
        st.subheader("🏫 معلومات المدرسة")
        
        school_name = st.text_input(
            "اسم المدرسة",
            value=school_info.get('school_name', ''),
            key="school_name",
            help="سيظهر في جميع التقارير المصدرة"
        )
        
        st.markdown("---")
        st.subheader("👥 القيادات المدرسية")
        
        projects_coordinator = st.text_input(
            "منسق المشاريع",
            value=school_info.get('projects_coordinator', ''),
            key="projects_coordinator"
        )
        
        academic_deputy = st.text_input(
            "النائب الأكاديمي",
            value=school_info.get('academic_deputy', ''),
            key="academic_deputy"
        )
        
        admin_deputy = st.text_input(
            "النائب الإداري",
            value=school_info.get('admin_deputy', ''),
            key="admin_deputy"
        )
        
        principal = st.text_input(
            "مدير المدرسة",
            value=school_info.get('principal', ''),
            key="principal"
        )
        
        email = st.text_input(
            "البريد الإلكتروني",
            value=school_info.get('email', ''),
            key="email"
        )
        
        st.markdown("---")
        st.subheader("🖼️ شعار الوزارة")
        
        moe_logo_file = st.file_uploader(
            "رفع شعار الوزارة",
            type=['png', 'jpg', 'jpeg'],
            help="سيظهر في رأس التقارير المصدرة",
            key="moe_logo_uploader"
        )
        
        if moe_logo_file is not None:
            # Save logo to assets folder
            assets_path = Path(__file__).parent / 'enjaz' / 'assets'
            assets_path.mkdir(exist_ok=True)
            logo_path = assets_path / 'ministry_logo.png'
            
            with open(logo_path, 'wb') as f:
                f.write(moe_logo_file.getbuffer())
            
            st.success("✅ تم حفظ شعار الوزارة بنجاح")
            st.image(moe_logo_file, width=150)
        
        st.markdown("---")
        st.subheader("👩‍🏫 بيانات المعلمين")
        
        teachers_file = st.file_uploader(
            "رفع ملف بيانات المعلمين (Excel/CSV)",
            type=['xlsx', 'xls', 'csv'],
            help="الملف يجب أن يحتوي على: اسم المعلم - المستوى - الشعبة - المادة - البريد الإلكتروني",
            key="teachers_file_uploader"
        )
        
        if teachers_file is not None:
            try:
                # Read teachers data
                if teachers_file.name.endswith('.csv'):
                    teachers_df = pd.read_csv(teachers_file)
                else:
                    teachers_df = pd.read_excel(teachers_file)
                
                # Save to session state
                st.session_state['teachers_data'] = teachers_df
                
                # Save to file
                data_path = Path(__file__).parent / 'enjaz' / 'data'
                data_path.mkdir(exist_ok=True)
                teachers_path = data_path / 'teachers.xlsx'
                teachers_df.to_excel(teachers_path, index=False)
                
                st.success(f"✅ تم تحميل بيانات {len(teachers_df)} معلم")
                
                # Display preview
                with st.expander("👁️ معاينة البيانات"):
                    st.dataframe(teachers_df.head(), use_container_width=True)
                    
            except Exception as e:
                st.error(f"❌ خطأ في قراءة الملف: {str(e)}")
        
        st.markdown("---")
        
        if st.button("💾 حفظ جميع الإعدادات", type="primary", use_container_width=True):
            save_school_info({
                'school_name': school_name,
                'projects_coordinator': projects_coordinator,
                'academic_deputy': academic_deputy,
                'admin_deputy': admin_deputy,
                'principal': principal,
                'email': email,
                'vision': school_info.get('vision', '')
            })
            st.success("✅ تم حفظ جميع الإعدادات بنجاح!")
            st.rerun()


def main():
    """Main application function."""
    # Apply professional design
    apply_professional_design()
    
    # Render professional header
    render_professional_header()
    
    # Sidebar
    st.sidebar.title("📊 القائمة الرئيسية")
    
    # School info settings
    school_info_settings()
    
    # File upload
    st.sidebar.subheader("📁 رفع الملفات")
    uploaded_files = st.sidebar.file_uploader(
        "اختر ملفات Excel",
        type=['xlsx', 'xls'],
        accept_multiple_files=True,
        help="يمكنك رفع ملف واحد أو أكثر"
    )
    
    if not uploaded_files:
        st.info("👈 الرجاء رفع ملفات Excel من القائمة الجانبية للبدء")
        render_professional_footer()
        return
    
    # Process files
    with st.spinner("⏳ جاري معالجة الملفات..."):
        qatar_tz = pytz.timezone('Asia/Qatar')
        today = date.today()
        
        all_data = aggregate_lms_files(uploaded_files, today=today)
    
    if not all_data:
        st.error("❌ لم يتم العثور على بيانات صالحة في الملفات المرفوعة.")
        render_professional_footer()
        return
    
    st.success(f"✅ تم تحميل {len(all_data)} ورقة عمل بنجاح!")
    
    # Main navigation
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 لوحة المعلومات",
        "📈 الرسوم البيانية",
        "📚 تقرير الصف/المادة",
        "🏫 ملف الطالب",
        "📥 التقارير الفردية",
        "🏫 تقرير المدرسة",
        "📊 التصدير التحليلي"
    ])
    
    # Tab 1: Dashboard
    with tab1:
        st.header("📊 لوحة المعلومات الرئيسية")
        
        kpis = calculate_weekly_kpis(all_data)
        
        # Calculate fallback values from data directly
        total_completed = sum(s['completed'] for d in all_data for s in d['students'])
        total_due = sum(s['total_due'] for d in all_data for s in d['students'])
        total_missing = sum(s['not_submitted'] for d in all_data for s in d['students'])
        total_students = sum(len(d['students']) for d in all_data)
        
        # Use .get() with fallbacks
        val_students = kpis.get('total_students', total_students)
        val_completed = kpis.get('total_assessments_completed', total_completed)
        val_due = kpis.get('total_assessments', total_due)
        val_missing = kpis.get('total_not_submitted', total_missing)
        val_avg = kpis.get('school_completion_avg', round(100.0 * total_completed / max(total_due, 1), 1))
        
        # Professional metric cards
        col1, col2, col3, col4 = st.columns(4)
        
        from enjaz.analysis import get_band
        school_band = get_band(val_avg)
        
        with col1:
            card_html = get_metric_card_html(
                title="👥 إجمالي الطلاب",
                value=val_students,
                subtitle="طالب"
            )
            st.markdown(card_html, unsafe_allow_html=True)
        
        with col2:
            card_html = get_metric_card_html(
                title="🎯 متوسط الإنجاز",
                value=f"{val_avg:.1f}%",
                subtitle="نسبة الحل",
                badge=school_band
            )
            st.markdown(card_html, unsafe_allow_html=True)
        
        with col3:
            card_html = get_metric_card_html(
                title="📊 إجمالي التقييمات",
                value=val_due,
                subtitle="تقييم مستحق"
            )
            st.markdown(card_html, unsafe_allow_html=True)
        
        with col4:
            completion_pct = round(100.0 * val_completed / max(val_due, 1), 1)
            card_html = get_metric_card_html(
                title="✅ التقييمات المُنجزة",
                value=val_completed,
                subtitle=f"{completion_pct}% من الإجمالي"
            )
            st.markdown(card_html, unsafe_allow_html=True)
        
        # Comprehensive dashboard
        st.subheader("📈 لوحة المعلومات الشاملة")
        try:
            fig = create_comprehensive_dashboard(all_data)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"⚠️ خطأ في إنشاء لوحة المعلومات: {str(e)}")
            st.info("📊 البيانات متوفرة في التبويبات الأخرى")
    
    # Tab 2: Charts
    with tab2:
        st.header("📈 الرسوم البيانية التفاعلية")
        
        chart_type = st.selectbox(
            "اختر نوع الرسم البياني",
            ["توزيع الفئات", "مقارنة الشعب", "مقارنة المواد"]
        )
        
        try:
            if chart_type == "توزيع الفئات":
                fig = create_band_distribution_chart(all_data)
            elif chart_type == "مقارنة الشعب":
                fig = create_class_comparison_chart(all_data)
            else:
                fig = create_subject_comparison_chart(all_data)
            
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"⚠️ خطأ في إنشاء الرسم البياني: {str(e)}")
            st.info("📈 يرجى التأكد من رفع الملفات بشكل صحيح")
    
    # Tab 3: Class/Subject Report - Horizontal View
    with tab3:
        st.header("📚 تقرير الصف والمادة - عرض أفقي")
        
        st.info("""
        📌 **تقرير شامل لجميع الطلاب**
        
        يعرض هذا التقرير جميع الطلاب مع تفاصيل أدائهم في جميع المواد بشكل أفقي:
        - اسم الطالب | الصف | الشعبة
        - لكل مادة: إجمالي التقييمات | المنجز | نسبة الحل
        """)
        
        # Use school_report module to create horizontal report
        from enjaz.school_report import create_horizontal_school_report
        
        try:
            # Create horizontal report
            horizontal_df = create_horizontal_school_report(all_data)
            
            if horizontal_df.empty:
                st.warning("⚠️ لا توجد بيانات للعرض")
            else:
                # Display statistics
                st.subheader("📊 إحصائيات عامة")
                
                col1, col2, col3 = st.columns(3)
                
                total_students = len(horizontal_df)
                avg_completion = horizontal_df['نسبة الحل العامة (%)'].mean()
                
                with col1:
                    st.metric("إجمالي الطلاب", total_students)
                
                with col2:
                    st.metric("متوسط الإنجاز", f"{avg_completion:.1f}%")
                
                with col3:
                    band = get_band(avg_completion)
                    st.metric("الفئة العامة", band)
                
                # Display horizontal table
                st.subheader("📋 تفاصيل جميع الطلاب")
                st.dataframe(horizontal_df, use_container_width=True, height=600)
                
                # Export option
                st.subheader("📄 تصدير التقرير")
                
                from enjaz.school_report import export_school_report_to_excel
                import tempfile
                import os
                
                if st.button("📅 تصدير إلى Excel"):
                    with tempfile.TemporaryDirectory() as tmpdir:
                        excel_path = os.path.join(tmpdir, 'تقرير_الصف_والمادة.xlsx')
                        export_school_report_to_excel(horizontal_df, excel_path)
                        
                        with open(excel_path, 'rb') as f:
                            st.download_button(
                                label="⬇️ تحميل التقرير",
                                data=f.read(),
                                file_name='تقرير_الصف_والمادة.xlsx',
                                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                            )
        
        except Exception as e:
            st.error(f"❌ حدث خطأ في إنشاء التقرير: {str(e)}")
            st.info("📊 البيانات متوفرة في التبويبات الأخرى")
    
    # Tab 4: Student Profile
    with tab4:
        st.header("👤 ملف الطالب الفردي")
        
        # Get all unique students with their grade and section
        student_info = {}
        for sheet_data in all_data:
            for student in sheet_data['students']:
                student_name = student['student_name']
                if student_name not in student_info:
                    student_info[student_name] = {
                        'grade': sheet_data.get('grade', ''),
                        'section': sheet_data.get('section', '')
                    }
        
        all_students = sorted(student_info.keys())
        selected_student = st.selectbox("اختر الطالب", all_students)
        
        if selected_student:
            # Collect student data across all subjects
            student_subjects = []
            
            for sheet_data in all_data:
                for student in sheet_data['students']:
                    if student['student_name'] == selected_student and student['has_due']:
                        student_subjects.append({
                            'subject': sheet_data.get('subject', sheet_data['sheet_name']),
                            'total_due': student['total_due'],
                            'completed': student['completed'],
                            'completion_rate': student['completion_rate']
                        })
            
            if student_subjects:
                # Overall stats
                total_due = sum(s['total_due'] for s in student_subjects)
                total_completed = sum(s['completed'] for s in student_subjects)
                overall_rate = 100 * total_completed / total_due if total_due > 0 else 0
                
                # Get student info
                student_grade = student_info[selected_student]['grade']
                student_section = student_info[selected_student]['section']
                student_band = get_band(overall_rate)
                student_emoji = get_band_emoji(overall_rate)
                
                # Display student info
                st.info(f"🏫 **الصف:** {student_grade} | 📚 **الشعبة:** {student_section}")
                
                st.subheader(f"📊 ملخص أداء: {selected_student}")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("إجمالي التقييمات", total_due)
                
                with col2:
                    st.metric("التقييمات المُنجزة", total_completed)
                
                with col3:
                    st.metric("نسبة الإنجاز", f"{overall_rate:.1f}%")
                
                with col4:
                    st.metric("الفئة", f"{student_emoji} {student_band}")
                
                # Subject breakdown
                st.subheader("📚 التفصيل حسب المواد")
                
                subjects_df = pd.DataFrame(student_subjects)
                subjects_df.columns = ['المادة', 'الإجمالي', 'المُنجز', 'نسبة الإنجاز']
                subjects_df['نسبة الإنجاز'] = subjects_df['نسبة الإنجاز'].apply(lambda x: f"{x:.1f}%")
                
                st.dataframe(subjects_df, use_container_width=True)
    
    # Tab 5: Individual Reports
    with tab5:
        st.header("📥 التقارير الفردية")
        
        report_type = st.radio(
            "نوع التقرير",
            ["تقرير فردي للطالب", "تقرير فردي للمادة/الشعبة"]
        )
        
        if report_type == "تقرير فردي للطالب":
            # Get all students
            all_students = set()
            for sheet_data in all_data:
                for student in sheet_data['students']:
                    all_students.add(student['student_name'])
            
            selected_student = st.selectbox("اختر الطالب", sorted(all_students), key="report_student")
            
            # Get class and section (from first sheet)
            class_name = all_data[0].get('class_code', 'غير محدد').split('/')[0] if '/' in all_data[0].get('class_code', '') else 'غير محدد'
            section = all_data[0].get('class_code', 'غير محدد').split('/')[1] if '/' in all_data[0].get('class_code', '') else 'غير محدد'
            
            if st.button("📄 إنشاء التقرير"):
                with st.spinner("⏳ جاري إنشاء التقرير..."):
                    try:
                        pdf_buffer = create_student_individual_report(
                            selected_student,
                            all_data,
                            class_name,
                            section
                        )
                        
                        st.download_button(
                            label="⬇️ تحميل التقرير (PDF)",
                            data=pdf_buffer,
                            file_name=f"تقرير_{selected_student}.pdf",
                            mime="application/pdf"
                        )
                        
                        st.success("✅ تم إنشاء التقرير بنجاح!")
                    except Exception as e:
                        st.error(f"❌ حدث خطأ: {str(e)}")
        
        else:
            # Class/Subject report
            sheet_names = [f"{d['subject']} - {d.get('class_code', '')}" for d in all_data]
            selected_sheet = st.selectbox("اختر المادة والشعبة", sheet_names, key="report_sheet")
            
            if st.button("📄 إنشاء التقرير"):
                with st.spinner("⏳ جاري إنشاء التقرير..."):
                    try:
                        sheet_index = sheet_names.index(selected_sheet)
                        sheet_data = all_data[sheet_index]
                        
                        pdf_buffer = create_class_subject_report(
                            sheet_data.get('subject', ''),
                            sheet_data.get('class_code', ''),
                            sheet_data
                        )
                        
                        st.download_button(
                            label="⬇️ تحميل التقرير (PDF)",
                            data=pdf_buffer,
                            file_name=f"تقرير_{selected_sheet}.pdf",
                            mime="application/pdf"
                        )
                        
                        st.success("✅ تم إنشاء التقرير بنجاح!")
                    except Exception as e:
                        st.error(f"❌ حدث خطأ: {str(e)}")
    
    # Tab 6: School Report
    with tab6:
        from tab6_school_report import render_school_report_tab
        render_school_report_tab(all_data)
    
    # Tab 7: Analytics Export
    with tab7:
        render_analytics_export_tab(all_data)

    # Render footer
    render_professional_footer()


if __name__ == "__main__":
    main()

