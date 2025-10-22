"""
Tab 6 content for School Report with comprehensive analytical layout and quantitative descriptive report.
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
from enjaz.department_recommendations import get_subject_recommendation


def get_school_level_recommendation(completion_rate):
    """Get school-level recommendation based on overall completion rate."""
    return get_subject_recommendation(completion_rate)


def calculate_school_statistics(all_data):
    """Calculate comprehensive school-level statistics."""
    stats = {
        'total_students': 0,
        'total_assessments': 0,
        'total_completed': 0,
        'completion_rate': 0.0,
        'band_distribution': {
            'البلاتينية': 0,
            'الذهبية': 0,
            'الفضية': 0,
            'البرونزية': 0,
            'يحتاج إلى تطوير من النظام': 0,
            'لا يستفيد من النظام': 0
        }
    }
    
    if not all_data:
        return stats
    
    # Track unique students
    unique_students = set()
    
    # Calculate totals from sheet_data structure
    for sheet_data in all_data:
        students = sheet_data.get('students', [])
        
        for student in students:
            # Track unique students
            student_name = student.get('student_name', '')
            unique_students.add(student_name)
            
            # Only count students with due assessments
            if student.get('has_due', False):
                total_due = student.get('total_due', 0)
                completed = student.get('completed', 0)
                
                stats['total_assessments'] += total_due
                stats['total_completed'] += completed
                
                # Calculate student's band
                completion_rate = student.get('completion_rate', 0.0)
                band = get_band(completion_rate)
                if band in stats['band_distribution']:
                    stats['band_distribution'][band] += 1
    
    # Set total unique students
    stats['total_students'] = len(unique_students)
    
    # Calculate overall completion rate
    if stats['total_assessments'] > 0:
        stats['completion_rate'] = (stats['total_completed'] / stats['total_assessments']) * 100
    
    return stats


def render_school_report_tab(all_data):
    """Render the school report tab with comprehensive analytical layout and quantitative report."""
    
    st.header("🏫 تقرير المدرسة - التقرير الكمي الوصفي")
    
    # Calculate school statistics
    school_stats = calculate_school_statistics(all_data)
    
    # Section 1: Quantitative Descriptive Report
    st.subheader("📊 التقرير الكمي الوصفي على مستوى المدرسة")
    
    # Check if there is any data to display
    if school_stats['total_assessments'] == 0:
        st.info("📊 **لا توجد تقييمات مستحقة حالياً**")
        st.markdown("""
        🔹 **الأسباب المحتملة:**
        - جميع التقييمات لم تصل إلى تاريخ الاستحقاق بعد
        - الفترة المحددة في فلتر التاريخ لا تحتوي على تقييمات
        - الملفات المرفوعة لا تحتوي على بيانات تقييمات
        
        💡 **الحلول المقترحة:**
        - قم بتعديل فلتر التاريخ في الشريط الجانبي
        - تأكد من رفع ملفات Excel الصحيحة
        - تحقق من وجود تقييمات في نظام LMS
        """)
    else:
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 إجمالي الطلاب", school_stats['total_students'])
        
        with col2:
            st.metric("📊 إجمالي التقييمات", school_stats['total_assessments'])
        
        with col3:
            st.metric("✅ التقييمات المُنجزة", school_stats['total_completed'])
        
        with col4:
            completion_rate = school_stats['completion_rate']
            overall_band = get_band(completion_rate)
            st.metric("🎯 نسبة الإنجاز الكلية", f"{completion_rate:.1f}%", delta=overall_band)
    
    # Band distribution and recommendations - only show if there's data
    if school_stats['total_assessments'] > 0:
        st.subheader("📈 توزيع الطلاب حسب فئات الأداء")
        
        band_df = pd.DataFrame([
            {'الفئة': band, 'عدد الطلاب': count, 'النسبة': f"{(count / max(school_stats['total_students'], 1) * 100):.1f}%"}
            for band, count in school_stats['band_distribution'].items()
        ])
        
        st.dataframe(band_df, use_container_width=True, hide_index=True)
        
        # Automatic recommendation based on completion rate
        st.subheader("💡 التوصية التلقائية")
        
        completion_rate = school_stats['completion_rate']
        auto_recommendation = get_school_level_recommendation(completion_rate)
        
        st.info(f"""
        **بناءً على نسبة الإنجاز الكلية ({completion_rate:.1f}%):**
        
        {auto_recommendation}
        """)
    
    # Section 2: Project Coordinator Actions
    st.subheader("📝 إجراءات منسق المشاريع")
    
    st.markdown("""
    يمكن لمنسق المشاريع كتابة الإجراءات المتخذة أو المخطط لها لتحسين الأداء على مستوى المدرسة.
    هذه الإجراءات ستُضاف تلقائياً كشريحة في العرض التقديمي.
    """)
    
    # Text area for coordinator actions
    coordinator_actions = st.text_area(
        "اكتب إجراءات منسق المشاريع هنا:",
        height=200,
        placeholder="""مثال:
- عقد اجتماع مع جميع رؤساء الأقسام لمناقشة نتائج التقرير
- تنظيم ورشة عمل للمعلمين حول استراتيجيات تحفيز الطلاب
- إطلاق حملة توعوية لأولياء الأمور حول أهمية المتابعة
- تفعيل نظام المكافآت للطلاب المتميزين
- متابعة أسبوعية للمواد ذات الأداء المنخفض"""
    )
    
    # Option to use pre-written actions
    use_template = st.checkbox("استخدام إجراءات جاهزة (نموذج)")
    
    if use_template:
        template_actions = f"""**الإجراءات المتخذة على مستوى المدرسة:**

**1. على المستوى الإداري:**
- عقد اجتماع طارئ مع جميع رؤساء الأقسام لمناقشة نتائج التقرير الكمي الوصفي
- تشكيل لجنة متابعة دائمة لرصد نسب الإنجاز أسبوعياً
- تخصيص موارد إضافية للأقسام ذات الأداء المنخفض

**2. على مستوى المعلمين:**
- تنظيم ورشة عمل لجميع المعلمين حول استراتيجيات رفع نسبة الإنجاز
- مشاركة أفضل الممارسات من الأقسام المتميزة
- توفير الدعم الفني للمعلمين في استخدام نظام قطر للتعليم

**3. على مستوى الطلاب:**
- إطلاق حملة تحفيزية تحت شعار "إنجاز 100%"
- تفعيل نظام المكافآت للطلاب المتميزين
- تنظيم جلسات توعوية للطلاب حول أهمية التقييمات الأسبوعية

**4. على مستوى أولياء الأمور:**
- إرسال تقارير دورية لأولياء الأمور عن أداء أبنائهم
- عقد اجتماع عام لأولياء الأمور لتوضيح أهمية المتابعة
- تفعيل قنوات التواصل المباشر (واتساب، بريد إلكتروني)

**5. المتابعة والتقييم:**
- إعداد تقرير متابعة أسبوعي لقياس التحسن
- مراجعة الإجراءات وتعديلها حسب النتائج
- تحديد موعد للتقرير القادم بعد شهر واحد

**التوقيع:**  
منسق المشاريع  
التاريخ: {pd.Timestamp.now().strftime('%Y-%m-%d')}
"""
        coordinator_actions = template_actions
        st.text_area("الإجراءات الجاهزة:", value=template_actions, height=400, disabled=True)
    
    # Button to add actions as a slide
    if st.button("➕ إضافة الإجراءات كشريحة في العرض التقديمي", type="primary"):
        if coordinator_actions.strip():
            # Store actions in session state
            st.session_state['coordinator_actions'] = coordinator_actions
            st.session_state['school_stats'] = school_stats
            st.success("✅ تم حفظ الإجراءات! يمكنك الآن إنشاء العرض التقديمي الشامل.")
            st.info("📊 ستتم إضافة شريحة جديدة تحتوي على إجراءات منسق المشاريع إلى العرض التقديمي.")
        else:
            st.warning("⚠️ الرجاء كتابة الإجراءات أولاً")
    
    st.markdown("---")
    
    # Section 3: Comprehensive Presentation
    st.subheader("🎬 العرض التقديمي الشامل")
    
    st.info("""
    📊 **عرض تقديمي متكامل يتضمن:**
    
    1️⃣ الإحصائيات الرئيسية على مستوى المدرسة
    2️⃣ توزيع الطلاب حسب الفئات
    3️⃣ التحليل العام للمواد
    4️⃣ تحليل تفصيلي لكل مادة
    5️⃣ التوصيات العامة
    6️⃣ توصية منسق المشاريع
    7️⃣ إجراءات منسق المشاريع
    """)
    
    # Input for coordinator recommendation
    st.markdown("**💡 توصية منسق المشاريع (اختياري):**")
    coordinator_recommendation = st.text_area(
        "اكتب توصيتك الخاصة هنا:",
        height=150,
        placeholder="مثال: بناءً على التحليل الشامل، أوصي بالتركيز على...",
        key="presentation_coordinator_recommendation"
    )
    
    # Get coordinator actions from session state or text area
    presentation_coordinator_actions = st.session_state.get('coordinator_actions', coordinator_actions)
    
    # Button to generate presentation
    if st.button("🎬 إنشاء العرض التقديمي الشامل", type="primary", use_container_width=True):
        with st.spinner("⏳ جاري إنشاء العرض التقديمي..."):
            try:
                from enjaz.school_comprehensive_presentation import (
                    calculate_school_statistics_for_presentation,
                    calculate_subject_statistics,
                    calculate_top_performers_statistics,
                    calculate_struggling_students_statistics,
                    get_presentation_outline
                )
                
                # Calculate statistics
                pres_school_stats = calculate_school_statistics_for_presentation(all_data)
                subject_stats = calculate_subject_statistics(all_data)
                top_performers_stats = calculate_top_performers_statistics(all_data)
                struggling_students_stats = calculate_struggling_students_statistics(all_data)
                
                # Check if there's data
                if pres_school_stats['total_assessments'] == 0:
                    st.warning("⚠️ لا توجد تقييمات مستحقة لإنشاء عرض تقديمي")
                else:
                    # Get outline
                    outline = get_presentation_outline(
                        pres_school_stats,
                        subject_stats,
                        top_performers_stats,
                        struggling_students_stats,
                        coordinator_recommendation,
                        presentation_coordinator_actions
                    )
                    
                    # Store in session state for slide generation
                    st.session_state['presentation_data'] = {
                        'school_stats': pres_school_stats,
                        'subject_stats': subject_stats,
                        'top_performers_stats': top_performers_stats,
                        'struggling_students_stats': struggling_students_stats,
                        'coordinator_recommendation': coordinator_recommendation,
                        'coordinator_actions': presentation_coordinator_actions,
                        'outline': outline
                    }
                    
                    st.success(f"✅ تم إعداد العرض التقديمي بنجاح! ({len(outline)} شريحة)")
                    st.info("⚡ يتم الآن إنشاء الشرائح...")
                    
                    # Display outline
                    with st.expander("👁️ معاينة محتوى العرض"):
                        for idx, slide in enumerate(outline, 1):
                            st.markdown(f"**{idx}. {slide['page_title']}**")
                            st.caption(slide['summary'])
                    
                    st.warning("🚧 ميزة إنشاء العرض التقديمي قيد التطوير. سيتم إضافتها في التحديث القادم.")
                    
            except Exception as e:
                st.error(f"❌ حدث خطأ: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
    
    st.markdown("---")
    
    # Section 4: Comprehensive Horizontal Report
    st.subheader("📋 التقرير التحليلي الشامل (عرض أفقي)")
    
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
        
        # Display the comprehensive report
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

