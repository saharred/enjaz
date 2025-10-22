"""
UI module for Enjaz application.
Handles Streamlit interface components and styling.
"""

import streamlit as st


# Qatar brand colors
QATAR_MAROON = "#6d3a46"
QATAR_GOLD = "#C9A227"


def apply_rtl_styling():
    """
    Apply RTL (Right-to-Left) styling and custom CSS for Arabic interface.
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
        
        * {
            font-family: 'Cairo', sans-serif !important;
        }
        
        html, body, [class*="css"] {
            direction: rtl;
            text-align: right;
        }
        
        .stApp {
            background-color: #FFFFFF;
        }
        
        /* Header styling */
        .main-header {
            background: linear-gradient(135deg, #6d3a46 0%, #6B0F2A 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .main-header h1 {
            color: #C9A227;
            font-size: 3rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .main-header p {
            color: white;
            font-size: 1.2rem;
            margin-top: 0.5rem;
        }
        
        /* Footer styling */
        .main-footer {
            background-color: #6d3a46;
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-top: 3rem;
            text-align: center;
            font-size: 0.9rem;
            line-height: 1.8;
        }
        
        .main-footer a {
            color: #C9A227;
            text-decoration: none;
        }
        
        .main-footer a:hover {
            text-decoration: underline;
        }
        
        /* Card styling */
        .metric-card {
            background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
            padding: 1.5rem;
            border-radius: 10px;
            border-right: 5px solid #6d3a46;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .metric-card h3 {
            color: #6d3a46;
            margin-bottom: 0.5rem;
        }
        
        .metric-card .value {
            font-size: 2rem;
            font-weight: 700;
            color: #C9A227;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #6d3a46;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            background-color: #6B0F2A;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Table styling */
        .dataframe {
            direction: rtl;
            text-align: right;
        }
        
        /* File uploader */
        .stFileUploader {
            direction: rtl;
        }
        
        /* Sidebar */
        .css-1d391kg {
            direction: rtl;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            direction: rtl;
        }
        
        /* Success/Error messages */
        .stSuccess, .stError, .stWarning, .stInfo {
            direction: rtl;
            text-align: right;
        }
        
        /* Band badges */
        .band-badge {
            display: inline-block;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            color: white;
            margin: 0.2rem;
        }
        
        .band-platinum {
            background-color: #E5E4E2;
            color: #333;
        }
        
        .band-gold {
            background-color: #C9A227;
        }
        
        .band-silver {
            background-color: #C0C0C0;
            color: #333;
        }
        
        .band-bronze {
            background-color: #CD7F32;
        }
        
        .band-needs {
            background-color: #6d3a46;
        }
        </style>
    """, unsafe_allow_html=True)


def render_header():
    """
    Render the application header with branding.
    """
    st.markdown("""
        <div class="main-header">
            <h1>✅ إنجاز</h1>
            <p>نظام تحليل التقييمات الإلكترونية الأسبوعية على قطر للتعليم</p>
        </div>
    """, unsafe_allow_html=True)


def render_footer():
    """
    Render the application footer with copyright and developer info.
    """
    st.markdown("""
        <div class="main-footer">
            <p><strong>© 2025 — جميع الحقوق محفوظة</strong></p>
            <p><strong>مدرسة عثمان بن عفّان النموذجية للبنين</strong></p>
            <p><a href="mailto:Sahar.Osman@education.qa">Sahar.Osman@education.qa</a></p>
            <p><strong>رؤيتنا: "متعلم ريادي لتنمية مستدامة"</strong></p>
        </div>
    """, unsafe_allow_html=True)


def render_metric_card(title, value, subtitle=""):
    """
    Render a metric card.
    
    Args:
        title: Card title
        value: Main value to display
        subtitle: Optional subtitle
    """
    st.markdown(f"""
        <div class="metric-card">
            <h3>{title}</h3>
            <div class="value">{value}</div>
            <p>{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)


def render_band_badge(band):
    """
    Render a colored badge for performance band.
    
    Args:
        band: Band name
    
    Returns:
        str: HTML for badge
    """
    band_classes = {
        "Platinum": "band-platinum",
        "Gold": "band-gold",
        "Silver": "band-silver",
        "Bronze": "band-bronze",
        "Needs Improvement": "band-needs",
        "N/A": "band-silver"
    }
    
    band_arabic = {
        "Platinum": "بلاتينيوم",
        "Gold": "ذهبي",
        "Silver": "فضي",
        "Bronze": "برونزي",
        "Needs Improvement": "يحتاج إلى تطوير",
        "N/A": "غير متاح"
    }
    
    css_class = band_classes.get(band, "band-silver")
    arabic_name = band_arabic.get(band, band)
    
    return f'<span class="band-badge {css_class}">{arabic_name}</span>'


def show_welcome_screen():
    """
    Show welcome screen with instructions.
    """
    st.markdown("""
        ## 👋 مرحباً بك في نظام إنجاز
        
        ### 📋 نظرة عامة
        نظام **إنجاز** هو تطبيق متخصص لتحليل بيانات إكمال التقييمات الأسبوعية من ملفات Excel المُصدّرة من نظام إدارة التعلم في قطر.
        
        ### 🚀 كيفية الاستخدام
        
        1. **رفع الملفات**: قم برفع ملف Excel واحد أو أكثر يحتوي على بيانات التقييمات الأسبوعية
        2. **التحليل التلقائي**: سيقوم النظام بتحليل البيانات وحساب نسب الإكمال تلقائياً
        3. **التصنيف**: سيتم تصنيف الطلاب إلى 5 فئات أداء
        4. **التقارير**: استعرض التقارير التفصيلية والتوصيات المهنية
        5. **التصدير**: قم بتصدير التقارير إلى Excel أو PDF
        
        ### 📊 فئات الأداء
        
        - **🥇 بلاتينيوم**: 95% فأكثر
        - **🥇 ذهبي**: 85% - 94.99%
        - **🥈 فضي**: 70% - 84.99%
        - **🥉 برونزي**: 50% - 69.99%
        - **⚠️ يحتاج إلى تطوير**: أقل من 50%
        
        ### 📁 متطلبات ملفات Excel
        
        - كل ملف يمثل أسبوعاً واحداً من التقييمات
        - كل ورقة في الملف تمثل مادة/صفاً واحداً
        - الصف 1: عناوين التقييمات
        - الصف 3: تواريخ الاستحقاق
        - العمود A: أسماء الطلاب
        - الأعمدة من H فصاعداً: بيانات التقييمات
        
        ### ✅ ابدأ الآن
        
        استخدم القائمة الجانبية لرفع ملفات Excel والبدء في التحليل!
    """)


def create_sidebar():
    """
    Create sidebar with file upload and navigation.
    
    Returns:
        tuple: (uploaded_files, selected_view)
    """
    with st.sidebar:
        st.markdown("### 📁 رفع الملفات")
        
        # File size info
        st.caption("الحد الأقصى: 200 ميجابايت لكل ملف")
        
        uploaded_files = st.file_uploader(
            "اختر ملفات Excel",
            type=['xlsx', 'xls'],
            accept_multiple_files=True,
            help="قم برفع ملف واحد أو أكثر من ملفات Excel من نظام LMS"
        )
        
        # Instructions expander
        with st.expander("📖 تعليمات هامة"):
            st.markdown("""
            ### بنية الملف المطلوبة:
            
            يجب أن يحتوي ملف Excel على الأعمدة التالية:
            
            - **اسم الطالب** (نص)
            - **الصف** (نص)
            - **الشعبة** (نص)
            - **المادة** (نص)
            - **التقييم** (نص)
            - **الحالة** (مكتمل/غير مكتمل)
            - **التاريخ** (تاريخ)
            
            ### ملاحظات:
            - يجب أن تكون أسماء الأعمدة بالعربية
            - تأكد من عدم وجود صفوف فارغة
            - الملف يجب أن يكون بصيغة `.xlsx` أو `.xls`
            
            ### تحميل ملف نموذجي:
            """)
            
            # Download template button
            try:
                import os
                template_path = os.path.join(os.path.dirname(__file__), '..', 'template.xlsx')
                if os.path.exists(template_path):
                    with open(template_path, 'rb') as f:
                        st.download_button(
                            label="📥 تحميل ملف نموذجي",
                            data=f,
                            file_name="template_injaz.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
            except Exception as e:
                st.caption("⚠️ الملف النموذجي غير متوفر حالياً")
        
        st.markdown("---")
        
        st.markdown("### 🎯 العرض")
        selected_view = st.radio(
            "اختر نوع العرض",
            ["لوحة المعلومات", "تقرير الصف/المادة", "ملف الطالب", "التقارير والتصدير"],
            help="اختر نوع التقرير الذي تريد عرضه"
        )
        
        st.markdown("---")
        
        st.markdown("### ℹ️ معلومات")
        st.info("نظام إنجاز v1.0")
        
        return uploaded_files, selected_view

