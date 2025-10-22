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
from enjaz.teacher_report import (
    aggregate_teacher_data,
    create_teacher_report_dataframe,
    create_students_by_band_report,
    format_teacher_report_for_email,
    create_band_summary_table,
    export_teacher_report_to_excel
)

# Page configuration
st.set_page_config(
    page_title="إنجاز - نظام تحليل التقييمات",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Qatar brand colors
QATAR_MAROON = "#8A1538"
QATAR_GOLD = "#C9A227"


def get_base64_image(image_path):
    """Convert image to base64 for embedding in HTML."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None


def apply_custom_css():
    """Apply custom CSS with logos and branding."""
    assets_path = Path(__file__).parent / 'enjaz' / 'assets'
    
    # Get base64 encoded logos
    enjaz_logo_b64 = get_base64_image(assets_path / 'logo.png')
    moe_logo_b64 = get_base64_image(assets_path / 'moe_logo.png')
    qatar_lms_logo_b64 = get_base64_image(assets_path / 'qatar_lms_logo.png')
    
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    * {{
        font-family: 'Cairo', sans-serif !important;
    }}
    
    html, body, [class*="css"] {{
        direction: rtl;
        text-align: right;
    }}
    
    .stApp {{
        background-color: #FFFFFF;
    }}
    
    /* Custom Header */
    .custom-header {{
        background: linear-gradient(135deg, {QATAR_MAROON} 0%, #6B0F2A 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        position: relative;
    }}
    
    .header-logos {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }}
    
    .logo-left {{
        width: 80px;
        height: auto;
    }}
    
    .logo-center {{
        width: 120px;
        height: auto;
    }}
    
    .logo-right {{
        width: 60px;
        height: auto;
    }}
    
    .custom-header h1 {{
        color: {QATAR_GOLD};
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }}
    
    .custom-header .subtitle {{
        color: {QATAR_GOLD};
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }}
    
    .custom-header p {{
        color: white;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }}
    
    /* Metric Cards */
    .metric-card {{
        background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-right: 5px solid {QATAR_MAROON};
        margin-bottom: 1rem;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }}
    
    .metric-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }}
    
    .metric-card h3 {{
        color: {QATAR_MAROON};
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
    }}
    
    .metric-card .value {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {QATAR_GOLD};
        margin: 0.5rem 0;
    }}
    
    .metric-card .subtitle {{
        color: #666;
        font-size: 0.95rem;
    }}
    
    /* Footer */
    .custom-footer {{
        background-color: {QATAR_MAROON};
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-top: 3rem;
        text-align: center;
        font-size: 0.95rem;
        line-height: 1.8;
    }}
    
    .custom-footer a {{
        color: {QATAR_GOLD};
        text-decoration: none;
    }}
    
    .custom-footer a:hover {{
        text-decoration: underline;
    }}
    
    /* Buttons */
    .stButton>button {{
        background-color: {QATAR_MAROON};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s;
    }}
    
    .stButton>button:hover {{
        background-color: {QATAR_GOLD};
        color: {QATAR_MAROON};
        transform: scale(1.05);
    }}
    
    /* Sidebar */
    .css-1d391kg {{
        background-color: #f8f9fa;
    }}
    
    /* Tables */
    .dataframe {{
        font-size: 0.9rem;
    }}
    
    .dataframe th {{
        background-color: {QATAR_MAROON} !important;
        color: white !important;
        text-align: center !important;
    }}
    
    .dataframe td {{
        text-align: center !important;
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def render_header():
    """Render custom header with logos - New Design."""
    assets_path = Path(__file__).parent / 'enjaz' / 'assets'
    
    # Logos
    enjaz_logo_path = assets_path / 'logo.png'
    qatar_lms_logo_path = assets_path / 'qatar_lms_logo.png'
    
    # Get base64 encoded images
    enjaz_logo_b64 = get_base64_image(enjaz_logo_path) if enjaz_logo_path.exists() else ''
    qatar_logo_b64 = get_base64_image(qatar_lms_logo_path) if qatar_lms_logo_path.exists() else ''
    
    header_html = f"""
    <style>
    .enjaz-logos {{
        display: grid;
        grid-template-columns: 96px 1fr 96px;
        gap: 12px;
        align-items: center;
        max-width: 1100px;
        margin: 0 auto 8px auto;
        padding: 20px 0;
    }}
    .enjaz-logos img {{
        width: 100%;
        height: auto;
        object-fit: contain;
    }}
    .enjaz-title {{
        text-align: center;
        color: {QATAR_MAROON};
        font-weight: 800;
        font-size: 42px;
        font-family: 'Cairo', sans-serif;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}
    .enjaz-subtitle {{
        text-align: center;
        color: {QATAR_GOLD};
        font-weight: 700;
        font-size: 18px;
        font-family: 'Cairo', sans-serif;
        margin: 8px 0 4px 0;
    }}
    .enjaz-description {{
        text-align: center;
        color: #555;
        font-size: 16px;
        font-family: 'Cairo', sans-serif;
        margin: 0;
    }}
    </style>
    
    <div class="enjaz-logos">
        {'<img src="data:image/png;base64,' + enjaz_logo_b64 + '" alt="Enjaz"/>' if enjaz_logo_b64 else '<div></div>'}
        <div class="enjaz-title">إنجاز</div>
        {'<img src="data:image/png;base64,' + qatar_logo_b64 + '" alt="Qatar Education"/>' if qatar_logo_b64 else '<div></div>'}
    </div>
    
    <p class="enjaz-subtitle">ضمان تنمية رقمية مستدامة</p>
    <p class="enjaz-description">نظام تحليل التقييمات الإلكترونية الأسبوعية على قطر للتعليم</p>
    """
    
    st.markdown(header_html, unsafe_allow_html=True)


def render_footer():
    """Render custom footer."""
    footer_html = f"""
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
        
        st.subheader("معلومات المدرسة")
        
        school_name = st.text_input(
            "اسم المدرسة",
            value=school_info['school_name'],
            key="school_name"
        )
        
        projects_coordinator = st.text_input(
            "منسق المشاريع",
            value=school_info['projects_coordinator'],
            key="projects_coordinator"
        )
        
        academic_deputy = st.text_input(
            "النائب الأكاديمي",
            value=school_info['academic_deputy'],
            key="academic_deputy"
        )
        
        admin_deputy = st.text_input(
            "النائب الإداري",
            value=school_info['admin_deputy'],
            key="admin_deputy"
        )
        
        principal = st.text_input(
            "مدير المدرسة",
            value=school_info['principal'],
            key="principal"
        )
        
        email = st.text_input(
            "البريد الإلكتروني",
            value=school_info['email'],
            key="email"
        )
        
        if st.button("💾 حفظ الإعدادات"):
            save_school_info({
                'school_name': school_name,
                'projects_coordinator': projects_coordinator,
                'academic_deputy': academic_deputy,
                'admin_deputy': admin_deputy,
                'principal': principal,
                'email': email,
                'vision': school_info['vision']
            })
            st.success("✅ تم حفظ الإعدادات بنجاح!")
            st.rerun()


def main():
    """Main application function."""
    # Apply custom CSS
    apply_custom_css()
    
    # Render header
    render_header()
    
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
        render_footer()
        return
    
    # Process files
    with st.spinner("⏳ جاري معالجة الملفات..."):
        qatar_tz = pytz.timezone('Asia/Qatar')
        today = date.today()
        
        all_data = aggregate_lms_files(uploaded_files, today=today)
    
    if not all_data:
        st.error("❌ لم يتم العثور على بيانات صالحة في الملفات المرفوعة.")
        render_footer()
        return
    
    st.success(f"✅ تم تحميل {len(all_data)} ورقة عمل بنجاح!")
    
    # Main navigation
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 لوحة المعلومات",
        "📈 الرسوم البيانية",
        "📚 تقرير الصف/المادة",
        "👤 ملف الطالب",
        "📥 التقارير الفردية",
        "👩‍🏫 تقرير المعلم"
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
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>إجمالي الطلاب</h3>
                <div class="value">{val_students}</div>
                <div class="subtitle">طالب</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>متوسط الإنجاز</h3>
                <div class="value">{val_avg:.1f}%</div>
                <div class="subtitle">نسبة الحل</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>إجمالي التقييمات</h3>
                <div class="value">{val_due}</div>
                <div class="subtitle">تقييم مستحق</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>التقييمات المُنجزة</h3>
                <div class="value">{val_completed}</div>
                <div class="subtitle">تقييم</div>
            </div>
            """, unsafe_allow_html=True)
        
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
    
    # Tab 3: Class/Subject Report
    with tab3:
        st.header("📚 تقرير الصف والمادة")
        
        # Select sheet
        sheet_names = [f"{d['subject']} - {d.get('class_code', '')}" for d in all_data]
        selected_sheet = st.selectbox("اختر المادة والشعبة", sheet_names)
        
        if selected_sheet:
            sheet_index = sheet_names.index(selected_sheet)
            sheet_data = all_data[sheet_index]
            
            stats = calculate_class_stats(sheet_data)
            
            st.subheader(f"📊 إحصائيات: {selected_sheet}")
            
            col1, col2, col3 = st.columns(3)
            
            # Calculate student count from sheet_data
            student_count = len(sheet_data.get('students', []))
            avg_completion = stats.get('average_completion', 0.0)
            band = get_band(avg_completion)
            
            with col1:
                st.metric("عدد الطلاب", student_count)
            
            with col2:
                st.metric("متوسط الإنجاز", f"{avg_completion:.1f}%")
            
            with col3:
                st.metric("الفئة", band)
            
            # Student table
            st.subheader("📋 قائمة الطلاب")
            
            students_df = pd.DataFrame([
                {
                    'اسم الطالب': s['student_name'],
                    'الإجمالي': s['total_due'],
                    'المُنجز': s['completed'],
                    'المتبقي': s['not_submitted'],
                    'نسبة الإنجاز': f"{s['completion_rate']:.1f}%"
                }
                for s in sheet_data['students'] if s['has_due']
            ])
            
            st.dataframe(students_df, use_container_width=True)
    
    # Tab 4: Student Profile
    with tab4:
        st.header("👤 ملف الطالب الفردي")
        
        # Get all unique students
        all_students = set()
        for sheet_data in all_data:
            for student in sheet_data['students']:
                all_students.add(student['student_name'])
        
        selected_student = st.selectbox("اختر الطالب", sorted(all_students))
        
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
                
                st.subheader(f"📊 ملخص أداء: {selected_student}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("إجمالي التقييمات", total_due)
                
                with col2:
                    st.metric("التقييمات المُنجزة", total_completed)
                
                with col3:
                    st.metric("نسبة الإنجاز", f"{overall_rate:.1f}%")
                
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
    
    # Tab 6: Teacher Report
    with tab6:
        st.header("👩‍🏫 تقرير المعلم - اختيار متعدد")
        
        st.info("📌 يمكنك اختيار أكثر من مادة وشعبة لإنشاء تقرير شامل يتضمن أسماء الطلاب حسب فئاتهم")
        
        # Teacher name input
        teacher_name = st.text_input(
            "👤 اسم المعلم/ة",
            value="المعلم/ة",
            help="أدخل اسم المعلم ليظهر في التقرير"
        )
        
        # Multi-select for subjects/classes
        sheet_names = [f"{d['subject']} - {d.get('class_code', '')}" for d in all_data]
        
        selected_sheets = st.multiselect(
            "📚 اختر المواد والشعب (يمكن اختيار أكثر من واحدة)",
            options=sheet_names,
            default=sheet_names[:1] if sheet_names else [],
            help="اختر جميع المواد والشعب التي تدرسها"
        )
        
        if not selected_sheets:
            st.warning("⚠️ الرجاء اختيار مادة واحدة على الأقل")
        else:
            # Get indices of selected sheets
            selected_indices = [sheet_names.index(sheet) for sheet in selected_sheets]
            
            # Aggregate teacher data
            teacher_data = aggregate_teacher_data(all_data, selected_indices)
            
            # Display summary
            st.subheader("📊 ملخص التقرير")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📚 عدد المواد/الشعب", len(teacher_data['sheets']))
            
            with col2:
                st.metric("👥 إجمالي الطلاب", teacher_data['total_students'])
            
            with col3:
                st.metric("📝 إجمالي التقييمات", teacher_data['total_assessments'])
            
            with col4:
                st.metric("🎯 متوسط الإنجاز", f"{teacher_data['average_completion']:.1f}%")
            
            # Display selected subjects/classes
            st.subheader("📚 المواد والشعب المختارة")
            
            sheets_info = []
            for sheet in teacher_data['sheets']:
                sheets_info.append({
                    'المادة': sheet['subject'],
                    'الشعبة': sheet['class_code'],
                    'الصف': sheet.get('grade', ''),
                    'القسم': sheet.get('section', '')
                })
            
            sheets_df = pd.DataFrame(sheets_info)
            st.dataframe(sheets_df, use_container_width=True)
            
            # Band distribution summary
            st.subheader("📋 توزيع الطلاب حسب الفئات")
            
            band_summary_df = create_band_summary_table(teacher_data)
            st.dataframe(band_summary_df, use_container_width=True)
            
            # Students by band
            st.subheader("👥 أسماء الطلاب حسب الفئات")
            
            students_by_band = create_students_by_band_report(teacher_data)
            
            for band_label, data in students_by_band.items():
                with st.expander(f"{band_label} ({data['count']} طالب/ة)"):
                    # Display as numbered list
                    for i, student in enumerate(data['students'], 1):
                        st.write(f"{i}. {student}")
            
            # Detailed student table
            st.subheader("📋 تفاصيل جميع الطلاب")
            
            detailed_df = create_teacher_report_dataframe(teacher_data)
            st.dataframe(detailed_df, use_container_width=True)
            
            # Export options
            st.subheader("📥 تصدير التقرير")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Export to Excel
                if st.button("📄 تصدير إلى Excel"):
                    try:
                        import tempfile
                        import os
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                            excel_path = export_teacher_report_to_excel(
                                teacher_data,
                                tmp.name,
                                teacher_name
                            )
                            
                            with open(excel_path, 'rb') as f:
                                excel_data = f.read()
                            
                            st.download_button(
                                label="⬇️ تحميل ملف Excel",
                                data=excel_data,
                                file_name=f"تقرير_المعلم_{teacher_name}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                            
                            # Clean up temp file
                            os.unlink(excel_path)
                            
                            st.success("✅ تم إنشاء ملف Excel بنجاح!")
                    except Exception as e:
                        st.error(f"❌ حدث خطأ: {str(e)}")
            
            with col2:
                # Format for email
                if st.button("📧 تنسيق للإيميل"):
                    email_text = format_teacher_report_for_email(teacher_data, teacher_name)
                    
                    st.text_area(
                        "📧 نص التقرير (انسخ والصق في الإيميل)",
                        value=email_text,
                        height=400,
                        help="انسخ هذا النص والصقه في رسالة الإيميل"
                    )
                    
                    st.success("✅ تم تنسيق التقرير للإيميل!")
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()

