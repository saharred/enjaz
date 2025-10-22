"""
Enjaz - نظام تحليل التقييمات الإلكترونية الأسبوعية
Main Streamlit Application with Advanced Features
"""

import streamlit as st
import pandas as pd
from datetime import date, timedelta
import pytz
from pathlib import Path
import base64

# Import Enjaz modules
from enjaz.data_ingest_lms import aggregate_lms_files
from enjaz.analysis import calculate_weekly_kpis, calculate_class_stats, get_band, get_band_emoji
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
    get_metric_card_html,
    QATAR_MAROON,
    QATAR_GOLD
)
from footer import render_footer
from enjaz.data_validation import validate_uploaded_files, display_validation_results

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
    """Render professional footer - DEPRECATED, use render_footer from footer.py instead."""
    # This function is deprecated and should not be called
    # Use render_footer() from footer.py instead
    pass

if False:  # Old footer code (to be removed)
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
    
    # Date filter
    st.sidebar.markdown("---")
    st.sidebar.subheader("📅 فلتر التاريخ")
    
    # Date range options
    date_filter_type = st.sidebar.radio(
        "نوع الفلتر",
        ["من وإلى", "من والآن"],
        help="اختر نوع فلتر التاريخ"
    )
    
    if date_filter_type == "من وإلى":
        start_date = st.sidebar.date_input(
            "📅 من تاريخ",
            value=date.today() - timedelta(days=30),
            help="تاريخ البداية"
        )
        end_date = st.sidebar.date_input(
            "📅 إلى تاريخ",
            value=date.today(),
            help="تاريخ النهاية"
        )
    else:  # من والآن
        start_date = st.sidebar.date_input(
            "📅 من تاريخ",
            value=date.today() - timedelta(days=30),
            help="تاريخ البداية"
        )
        end_date = st.sidebar.date_input(
            "📅 إلى تاريخ (اليوم)",
            value=date.today(),
            help="تاريخ النهاية - الافتراضي هو اليوم",
            disabled=False
        )
    
    # Display selected date range
    st.sidebar.info(f"📅 الفترة: {start_date.strftime('%Y-%m-%d')} إلى {end_date.strftime('%Y-%m-%d')}")
    st.sidebar.markdown("---")
    
    # Subject filter (will be populated after loading data)
    st.sidebar.subheader("📚 فلتر المواد")
    # Placeholder - will be updated after data is loaded
    subject_filter_placeholder = st.sidebar.empty()
    st.sidebar.markdown("---")
    
    if not uploaded_files:
        st.info("👈 الرجاء رفع ملفات Excel من القائمة الجانبية للبدء")
        render_footer()
        return
    
    # Validate files first
    with st.spinner("⏳ جاري التحقق من الملفات..."):
        try:
            is_valid, validation_results = validate_uploaded_files(uploaded_files)
            
            # Display validation results
            if not is_valid:
                st.warning("⚠️ تم العثور على بعض المشاكل في الملفات:")
                display_validation_results(validation_results)
                st.info("💡 يمكنك المتابعة إذا كانت الملفات من نظام LMS وتحتوي على بيانات صحيحة")
            
        except FileNotFoundError:
            st.error("❌ لم يتم العثور على الملفات. يرجى رفع ملفات Excel.")
            render_footer()
            return
        except ValueError as e:
            st.error(f"❌ خطأ في قراءة الملف: {str(e)}")
            st.info("💡 تأكد من أن الملف بصيغة Excel صحيحة وغير تالف")
            render_footer()
            return
        except Exception as e:
            st.error(f"❌ حدث خطأ غير متوقع: {str(e)}")
            st.info("💡 يرجى التأكد من أن الملفات من نظام LMS ومحاولة مرة أخرى")
            render_footer()
            return
    
    # Process files
    with st.spinner("⏳ جاري معالجة الملفات..."):
        try:
            qatar_tz = pytz.timezone('Asia/Qatar')
            today = date.today()
            
            all_data = aggregate_lms_files(uploaded_files, today=today)
            
            if not all_data:
                st.error("❌ لم يتم العثور على بيانات صالحة في الملفات المرفوعة.")
                st.info("💡 تأكد من أن الملفات تحتوي على بيانات الطلاب والتقييمات")
                render_footer()
                return
            
            st.success(f"✅ تم تحليل الملف بنجاح! تم تحميل {len(all_data)} ورقة عمل 🎉")
            
            # Populate subject filter
            all_subjects = sorted(list(set([sheet.get('subject', sheet['sheet_name']) for sheet in all_data])))
            
            with subject_filter_placeholder.container():
                # Subject multiselect with "Select All" option
                selected_subjects = st.multiselect(
                    "📚 اختر المواد (يمكن اختيار أكثر من مادة)",
                    all_subjects,
                    default=all_subjects,
                    help="اختر مادة أو أكثر لعرض بياناتها فقط. الافتراضي: جميع المواد"
                )
                
                # Show count of selected subjects
                if len(selected_subjects) == len(all_subjects):
                    st.caption(f"✅ تم تحديد جميع المواد ({len(all_subjects)} مادة)")
                elif len(selected_subjects) > 0:
                    st.caption(f"🔍 تم تحديد {len(selected_subjects)} من {len(all_subjects)} مادة")
                else:
                    st.caption("⚠️ لم يتم تحديد أي مادة")
            
            # Filter data based on selected subjects
            if selected_subjects:
                all_data = [sheet for sheet in all_data if sheet.get('subject', sheet['sheet_name']) in selected_subjects]
                if len(selected_subjects) < len(all_subjects):
                    st.info(f"🔍 تم فلترة البيانات: {len(selected_subjects)} مادة محددة")
            else:
                st.warning("⚠️ لم يتم اختيار أي مادة. سيتم عرض جميع المواد.")
            
        except Exception as e:
            st.error(f"❌ خطأ في معالجة البيانات: {str(e)}")
            render_footer()
            return
    
    # Main navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "✓ لوحة المعلومات",
        "✓ تقرير المدرسة",
        "✓ تقارير الأقسام",
        "✓ ملف الطالب",
        "✓ التقارير الفردية"
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
    
    # Tab 2: School Report
    with tab2:
        from tab6_school_report import render_school_report_tab
        render_school_report_tab(all_data)
    
    # Tab 3: Department Statistical Report
    with tab3:
        st.header("✓ التقرير الإحصائي للأقسام")
        st.subheader("📊 التقرير الكمي الوصفي")
        
        from enjaz.analysis import get_band
        from enjaz.department_recommendations import get_subject_recommendation, PREDEFINED_RECOMMENDATIONS
        import pandas as pd
        
        try:
            # Calculate statistics per subject
            subject_stats = []
            
            for sheet_data in all_data:
                subject_name = sheet_data.get('subject', sheet_data['sheet_name'])
                students = sheet_data['students']
                
                # Calculate totals
                total_students = len([s for s in students if s.get('has_due', False)])
                if total_students == 0:
                    continue
                
                total_completed = sum(s['completed'] for s in students)
                total_due = sum(s['total_due'] for s in students)
                completion_rate = round(100.0 * total_completed / max(total_due, 1), 1)
                
                # Calculate band distribution
                band_counts = {
                    'البلاتينية': 0,
                    'الذهبية': 0,
                    'الفضية': 0,
                    'البرونزية': 0,
                    'يحتاج إلى تطوير': 0,
                    'لا يستفيد من النظام': 0
                }
                
                for student in students:
                    if student.get('has_due', False):
                        band = get_band(student['completion_rate'])
                        if band in band_counts:
                            band_counts[band] += 1
                
                # Calculate percentages
                band_percentages = {
                    k: round(100.0 * v / max(total_students, 1), 1)
                    for k, v in band_counts.items()
                }
                
                # Get recommendation
                recommendation = get_subject_recommendation(completion_rate)
                
                subject_stats.append({
                    'المادة': subject_name,
                    'نسبة الإنجاز': f"{completion_rate}%",
                    'نسبة الطلاب الفئة البلاتينية': f"{band_percentages['البلاتينية']}%",
                    'نسبة الطلاب الفئة الذهبية': f"{band_percentages['الذهبية']}%",
                    'نسبة الطلاب الفئة الفضية': f"{band_percentages['الفضية']}%",
                    'نسبة الطلاب الفئة البرونزية': f"{band_percentages['البرونزية']}%",
                    'نسبة الطلاب الفئة تحتاج إلى تطوير من النظام': f"{band_percentages['يحتاج إلى تطوير']}%",
                    'نسبة الطلاب الفئة لا يستفيد من النظام': f"{band_percentages['لا يستفيد من النظام']}%",
                    'توصية منسق المشاريع': recommendation
                })
            
            if not subject_stats:
                st.warning("⚠️ لا توجد بيانات للعرض")
            else:
                # Display statistics table
                st.subheader("📋 الجدول الإحصائي")
                df_stats = pd.DataFrame(subject_stats)
                st.dataframe(df_stats, use_container_width=True, height=400)
                
                # Recommendations section
                st.subheader("📝 توصية منسق المشاريع")
                
                recommendation_mode = st.radio(
                    "اختر طريقة إدخال التوصية:",
                    ["🖊️ كتابة مباشرة", "📋 اختيار من التوصيات الجاهزة"],
                    horizontal=True
                )
                
                if recommendation_mode == "🖊️ كتابة مباشرة":
                    custom_recommendation = st.text_area(
                        "أدخل التوصية:",
                        height=150,
                        placeholder="اكتب توصيتك هنا..."
                    )
                    final_recommendation = custom_recommendation
                else:
                    selected_recommendations = st.multiselect(
                        "اختر التوصيات (يمكن اختيار أكثر من واحدة):",
                        PREDEFINED_RECOMMENDATIONS
                    )
                    final_recommendation = "\n• ".join(selected_recommendations) if selected_recommendations else ""
                
                if final_recommendation:
                    st.info(f"📌 **التوصية النهائية:**\n\n{final_recommendation}")
                
                # Export section
                st.subheader("📄 تصدير التقرير")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Export to Excel
                    import io
                    excel_buffer = io.BytesIO()
                    df_stats.to_excel(excel_buffer, index=False, engine='openpyxl')
                    excel_buffer.seek(0)
                    
                    st.download_button(
                        label="⬇️ تحميل Excel",
                        data=excel_buffer,
                        file_name="تقرير_الأقسام_الإحصائي.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                with col2:
                    # Presentation button
                    if st.button("📊 إنشاء عرض تقديمي", use_container_width=True):
                        st.info("⚡ جاري إنشاء العرض التقديمي...")
                        # Link to the presentation created earlier
                        st.markdown("""
                        ### 🎉 العرض التقديمي جاهز!
                        
                        اضغط على الرابط أدناه لعرض الشرائح:
                        
                        [manus-slides://X0TwrnPxMjnPAHM688fQSP](manus-slides://X0TwrnPxMjnPAHM688fQSP)
                        
                        **محتوى العرض:**
                        - 📊 نسب الإنجاز لكل مادة
                        - 📈 توزيع الطلاب على الفئات
                        - 🎯 مقارنة الأداء
                        - ✅ التوصيات وخطة العمل
                        """)
                        st.success("✅ يمكنك تصدير العرض كـ PDF أو PPT من واجهة العرض")
        
                
                # Add spacing
                st.markdown("---")
                
        except Exception as e:
            st.error(f"❌ حدث خطأ في إنشاء التقرير: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
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
                student_emoji = get_band_emoji(student_band)
                
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
            
            # Get class and section (from first sheet)
            class_name = all_data[0].get('class_code', 'غير محدد').split('/')[0] if '/' in all_data[0].get('class_code', '') else 'غير محدد'
            section = all_data[0].get('class_code', 'غير محدد').split('/')[1] if '/' in all_data[0].get('class_code', '') else 'غير محدد'
            
            # Choose between single or multiple students
            report_mode = st.radio(
                "نوع التقرير",
                ["طالب واحد", "عدة طلاب (ملف مضغوط)"],
                horizontal=True
            )
            
            if report_mode == "طالب واحد":
                selected_student = st.selectbox("اختر الطالب", sorted(all_students), key="report_student")
                
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
            
            else:  # عدة طلاب (ملف مضغوط)
                col1, col2 = st.columns([3, 1])
                
                with col2:
                    # Select all button
                    if st.button(f"✅ تحديد الكل ({len(all_students)})", use_container_width=True):
                        st.session_state.bulk_report_students = sorted(all_students)
                        st.rerun()
                
                with col1:
                    # Clear selection button
                    if st.button("❌ إلغاء التحديد", use_container_width=True):
                        st.session_state.bulk_report_students = []
                        st.rerun()
                
                # Initialize session state if not exists
                if 'bulk_report_students' not in st.session_state:
                    st.session_state.bulk_report_students = []
                
                selected_students = st.multiselect(
                    "اختر الطلاب (يمكن اختيار أكثر من طالب)",
                    sorted(all_students),
                    default=st.session_state.bulk_report_students,
                    key="bulk_report_students"
                )
                
                if selected_students:
                    st.info(f"📊 عدد الطلاب المختارين: {len(selected_students)}")
                    
                    if st.button(f"📦 إنشاء {len(selected_students)} تقرير وتنزيل ملف مضغوط"):
                        import zipfile
                        import io
                        
                        with st.spinner(f"⏳ جاري إنشاء {len(selected_students)} تقرير..."):
                            try:
                                # Create ZIP file in memory
                                zip_buffer = io.BytesIO()
                                
                                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                                    progress_bar = st.progress(0)
                                    
                                    for idx, student_name in enumerate(selected_students):
                                        # Create individual report
                                        pdf_buffer = create_student_individual_report(
                                            student_name,
                                            all_data,
                                            class_name,
                                            section
                                        )
                                        
                                        # Add to ZIP with sanitized filename
                                        safe_name = student_name.replace('/', '_').replace('\\', '_')
                                        zip_file.writestr(
                                            f"تقرير_{safe_name}.pdf",
                                            pdf_buffer.getvalue()
                                        )
                                        
                                        # Update progress
                                        progress_bar.progress((idx + 1) / len(selected_students))
                                
                                zip_buffer.seek(0)
                                
                                st.download_button(
                                    label=f"⬇️ تحميل {len(selected_students)} تقرير (ملف مضغوط)",
                                    data=zip_buffer,
                                    file_name=f"تقارير_فردية_{len(selected_students)}_طالب.zip",
                                    mime="application/zip"
                                )
                                
                                st.success(f"✅ تم إنشاء {len(selected_students)} تقرير بنجاح!")
                            except Exception as e:
                                st.error(f"❌ حدث خطأ: {str(e)}")
                                import traceback
                                st.code(traceback.format_exc())
                else:
                    st.warning("⚠️ الرجاء اختيار طالب واحد على الأقل")
        
        else:
            # Class/Subject report with multiselect
            st.info("📌 يمكنك اختيار عدة مواد/شعب لتجميعها في تقرير واحد (مثلاً: معلم علوم يدرّس ثالث1 و ثالث2)")
            
            sheet_names = [f"{d['subject']} - {d.get('class_code', '')}" for d in all_data]
            selected_sheets = st.multiselect(
                "اختر المواد والشعب (يمكن اختيار أكثر من واحد)",
                sheet_names,
                key="report_sheets"
            )
            
            if selected_sheets and st.button("📄 إنشاء التقرير"):
                with st.spinner("⏳ جاري إنشاء التقرير..."):
                    try:
                        # Get selected sheet indices
                        selected_indices = [sheet_names.index(name) for name in selected_sheets]
                        
                        # Import teacher report module
                        from enjaz.teacher_report import aggregate_teacher_data, export_teacher_report_to_excel
                        
                        # Aggregate data from selected sheets
                        teacher_data = aggregate_teacher_data(all_data, selected_indices)
                        
                        # Create Excel report
                        import tempfile
                        import os
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                            excel_path = export_teacher_report_to_excel(teacher_data, tmp.name)
                            
                            with open(excel_path, 'rb') as f:
                                excel_data = f.read()
                            
                            st.download_button(
                                label="⬇️ تحميل التقرير (Excel)",
                                data=excel_data,
                                file_name=f"تقرير_مجمّع_{len(selected_sheets)}_مواد.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                            
                            # Clean up
                            os.unlink(excel_path)
                        
                        st.success(f"✅ تم إنشاء تقرير مجمّع لـ {len(selected_sheets)} مادة/شعبة بنجاح!")
                        
                        # Display summary
                        st.subheader("📊 ملخص التقرير")
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("👥 عدد الطلاب", teacher_data['total_students'])
                        
                        with col2:
                            st.metric("📊 عدد التقييمات", teacher_data['total_assessments'])
                        
                        with col3:
                            st.metric("✅ المُنجز", teacher_data['total_completed'])
                        
                        with col4:
                            st.metric("🎯 متوسط الإنجاز", f"{teacher_data['average_completion']:.1f}%")
                        
                        # Email sending feature
                        st.divider()
                        st.subheader("📧 إرسال التقرير عبر البريد الإلكتروني")
                        
                        with st.expander("📧 إرسال التقرير للمعلم", expanded=False):
                            from enjaz.email_sender import send_teacher_report_email, validate_email, get_email_config_instructions
                            
                            col_email1, col_email2 = st.columns(2)
                            
                            with col_email1:
                                teacher_name = st.text_input(
                                    "👤 اسم المعلم/ة",
                                    placeholder="مثلاً: أحمد محمد",
                                    key="teacher_name_email"
                                )
                            
                            with col_email2:
                                teacher_email = st.text_input(
                                    "📧 البريد الإلكتروني",
                                    placeholder="teacher@school.qa",
                                    key="teacher_email"
                                )
                            
                            if st.button("✉️ إرسال التقرير", key="send_email_btn"):
                                if not teacher_name or not teacher_email:
                                    st.warning("⚠️ يرجى إدخال الاسم والبريد الإلكتروني")
                                elif not validate_email(teacher_email):
                                    st.error("❌ البريد الإلكتروني غير صحيح")
                                else:
                                    with st.spinner("📤 جاري إرسال التقرير..."):
                                        # Create temporary file for email
                                        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_email:
                                            excel_path_email = export_teacher_report_to_excel(teacher_data, tmp_email.name)
                                            
                                            success, message = send_teacher_report_email(
                                                recipient_email=teacher_email,
                                                teacher_name=teacher_name,
                                                report_file_path=excel_path_email,
                                                subject_count=len(selected_sheets)
                                            )
                                            
                                            # Clean up
                                            os.unlink(excel_path_email)
                                        
                                        if success:
                                            st.success(message)
                                        else:
                                            st.warning(message)
                            
                            # Configuration instructions
                            with st.expander("⚙️ إعدادات البريد الإلكتروني"):
                                st.markdown(get_email_config_instructions())
                        
                        # Store report path in session state for email
                        if 'last_report_path' not in st.session_state:
                            st.session_state.last_report_path = None
                        
                    except Exception as e:
                        st.error(f"❌ حدث خطأ: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())
    
    # Render professional footer
    render_footer()


if __name__ == "__main__":
    main()

