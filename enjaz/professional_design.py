"""
Professional Design Module for Injaz
Flat Design with Qatar Education Branding
"""

# Qatar Official Colors
QATAR_MAROON = "#6d3a46"
QATAR_GOLD = "#C9A227"
QATAR_WHITE = "#FFFFFF"

# Band Colors (from analysis.py)
BAND_COLORS = {
    'البلاتينية': '#E5E4E2',  # Platinum
    'الذهبية': '#FFD700',     # Gold
    'الفضية': '#C0C0C0',      # Silver
    'البرونزية': '#CD7F32',   # Bronze
    'يحتاج إلى تطوير': '#FF6600',  # Orange
    'لا يستفيد من النظام': '#C00000'   # Red
}


def get_professional_css():
    """
    Get professional CSS for Flat Design interface.
    
    Returns:
        str: CSS code
    """
    
    css = f"""
    <style>
    /* ============================================
       PROFESSIONAL FLAT DESIGN FOR INJAZ
       Qatar Education Branding
       ============================================ */
    
    /* Import Cairo Font */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');
    
    /* ============================================
       GLOBAL STYLES
       ============================================ */
    
    * {{
        font-family: 'Cairo', sans-serif !important;
    }}
    
    html, body, [class*="css"] {{
        direction: rtl;
        text-align: right;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }}
    
    /* ============================================
       HEADER SECTION
       ============================================ */
    
    .professional-header {{
        background: linear-gradient(135deg, {QATAR_MAROON} 0%, #6B0F2A 100%);
        padding: 2.5rem 2rem;
        border-radius: 0 0 30px 30px;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 24px rgba(138, 21, 56, 0.3);
        position: relative;
        overflow: hidden;
    }}
    
    .professional-header::before {{
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 400px;
        height: 400px;
        background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><polygon points="50,15 61,35 82,35 67,50 73,70 50,57 27,70 33,50 18,35 39,35" fill="{QATAR_GOLD.replace("#", "%23")}" opacity="0.1"/></svg>');
        background-size: 200px;
        opacity: 0.3;
    }}
    
    .professional-header .logo-side {{
        position: relative;
        z-index: 1;
    }}
    
    .professional-header .logo-side img {{
        max-height: 100px;
        width: auto;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
    }}
    
    .professional-header .text-side {{
        position: relative;
        z-index: 1;
    }}
    
    .professional-header h1 {{
        color: {QATAR_WHITE};
        font-size: 3rem;
        font-weight: 800;
        margin: 0.5rem 0;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
        letter-spacing: 1px;
        position: relative;
        z-index: 1;
    }}
    
    .professional-header .subtitle {{
        color: {QATAR_GOLD};
        font-size: 1.3rem;
        font-weight: 600;
        margin: 0.5rem 0;
        position: relative;
        z-index: 1;
    }}
    
    .professional-header .tagline {{
        color: rgba(255, 255, 255, 0.9);
        font-size: 1rem;
        margin-top: 1rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }}
    
    /* ============================================
       SIDEBAR DESIGN
       ============================================ */
    
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {QATAR_WHITE} 0%, #f8f9fa 100%);
        border-left: 3px solid {QATAR_MAROON};
    }}
    
    [data-testid="stSidebar"] .sidebar-content {{
        padding: 1rem;
    }}
    
    /* Sidebar Headers */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        color: {QATAR_MAROON};
        font-weight: 700;
        border-bottom: 2px solid {QATAR_GOLD};
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }}
    
    /* Sidebar File Uploader */
    [data-testid="stSidebar"] .stFileUploader {{
        background: white;
        border: 2px dashed {QATAR_MAROON};
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }}
    
    /* Sidebar Text Inputs */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea {{
        border: 2px solid #dee2e6;
        border-radius: 8px;
        padding: 0.75rem;
        transition: all 0.3s;
    }}
    
    [data-testid="stSidebar"] input:focus,
    [data-testid="stSidebar"] textarea:focus {{
        border-color: {QATAR_MAROON};
        box-shadow: 0 0 0 3px rgba(138, 21, 56, 0.1);
    }}
    
    /* ============================================
       CARD COMPONENTS
       ============================================ */
    
    .metric-card {{
        background: white;
        padding: 2rem 1.5rem;
        border-radius: 16px;
        border-right: 5px solid {QATAR_MAROON};
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: {QATAR_GOLD};
        opacity: 0.05;
        border-radius: 50%;
        transform: translate(30%, -30%);
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(138, 21, 56, 0.15);
        border-right-width: 8px;
    }}
    
    .metric-card h3 {{
        color: {QATAR_MAROON};
        margin-bottom: 0.75rem;
        font-size: 1.1rem;
        font-weight: 700;
    }}
    
    .metric-card .value {{
        font-size: 3rem;
        font-weight: 800;
        color: {QATAR_MAROON};
        margin: 0.5rem 0;
        line-height: 1;
    }}
    
    .metric-card .subtitle {{
        color: #6c757d;
        font-size: 0.95rem;
        font-weight: 500;
    }}
    
    .metric-card .badge {{
        display: inline-block;
        background: {QATAR_GOLD};
        color: {QATAR_MAROON};
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }}
    
    /* Info Card */
    .info-card {{
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-right: 5px solid #1976d2;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }}
    
    .info-card h4 {{
        color: #1565c0;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }}
    
    .info-card p {{
        color: #424242;
        margin: 0.25rem 0;
        line-height: 1.6;
    }}
    
    /* ============================================
       BUTTONS
       ============================================ */
    
    .stButton>button {{
        background: linear-gradient(135deg, {QATAR_MAROON} 0%, #6B0F2A 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(138, 21, 56, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .stButton>button:hover {{
        background: linear-gradient(135deg, {QATAR_GOLD} 0%, #B8A020 100%);
        color: {QATAR_MAROON};
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(201, 162, 39, 0.4);
    }}
    
    .stButton>button:active {{
        transform: translateY(0);
    }}
    
    /* Download Button */
    .stDownloadButton>button {{
        background: linear-gradient(135deg, {QATAR_GOLD} 0%, #B8A020 100%);
        color: {QATAR_MAROON};
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(201, 162, 39, 0.3);
    }}
    
    .stDownloadButton>button:hover {{
        background: linear-gradient(135deg, {QATAR_MAROON} 0%, #6B0F2A 100%);
        color: white;
        transform: translateY(-2px);
    }}
    
    /* ============================================
       TABLES
       ============================================ */
    
    .dataframe {{
        font-size: 0.9rem;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }}
    
    .dataframe thead tr {{
        background: linear-gradient(135deg, {QATAR_MAROON} 0%, #6B0F2A 100%);
    }}
    
    .dataframe th {{
        background-color: {QATAR_MAROON} !important;
        color: white !important;
        text-align: center !important;
        font-weight: 700 !important;
        padding: 1rem 0.5rem !important;
        border: none !important;
    }}
    
    .dataframe td {{
        text-align: center !important;
        padding: 0.75rem 0.5rem !important;
        border-bottom: 1px solid #e9ecef !important;
    }}
    
    .dataframe tbody tr:hover {{
        background-color: rgba(138, 21, 56, 0.05) !important;
    }}
    
    .dataframe tbody tr:nth-child(even) {{
        background-color: #f8f9fa;
    }}
    
    /* ============================================
       TABS
       ============================================ */
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: white;
        padding: 0.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        border-radius: 8px;
        color: {QATAR_MAROON};
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: rgba(138, 21, 56, 0.1);
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {QATAR_MAROON} 0%, #6B0F2A 100%);
        color: white !important;
        box-shadow: 0 4px 12px rgba(138, 21, 56, 0.3);
    }}
    
    /* ============================================
       EXPANDERS
       ============================================ */
    
    .streamlit-expanderHeader {{
        background-color: white;
        border: 2px solid {QATAR_MAROON};
        border-radius: 10px;
        font-weight: 700;
        color: {QATAR_MAROON};
        padding: 1rem;
    }}
    
    .streamlit-expanderHeader:hover {{
        background-color: rgba(138, 21, 56, 0.05);
    }}
    
    /* ============================================
       ALERTS & MESSAGES
       ============================================ */
    
    .stAlert {{
        border-radius: 12px;
        border-right: 5px solid;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }}
    
    .stSuccess {{
        background-color: #d4edda;
        border-color: #28a745;
        color: #155724;
    }}
    
    .stInfo {{
        background-color: #d1ecf1;
        border-color: #17a2b8;
        color: #0c5460;
    }}
    
    .stWarning {{
        background-color: #fff3cd;
        border-color: #ffc107;
        color: #856404;
    }}
    
    .stError {{
        background-color: #f8d7da;
        border-color: #dc3545;
        color: #721c24;
    }}
    
    /* ============================================
       FOOTER
       ============================================ */
    
    .professional-footer {{
        background: linear-gradient(135deg, {QATAR_MAROON} 0%, #6B0F2A 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 30px 30px 0 0;
        margin: 3rem -1rem -1rem -1rem;
        text-align: center;
        box-shadow: 0 -8px 24px rgba(138, 21, 56, 0.2);
    }}
    
    .professional-footer h3 {{
        color: {QATAR_GOLD};
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }}
    
    .professional-footer p {{
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.8;
        margin: 0.5rem 0;
    }}
    
    .professional-footer a {{
        color: {QATAR_GOLD};
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s;
    }}
    
    .professional-footer a:hover {{
        color: white;
        text-decoration: underline;
    }}
    
    .professional-footer .divider {{
        width: 100px;
        height: 3px;
        background: {QATAR_GOLD};
        margin: 1.5rem auto;
        border-radius: 2px;
    }}
    
    /* ============================================
       BAND BADGES
       ============================================ */
    
    .band-badge {{
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }}
    
    .band-platinum {{
        background-color: {BAND_COLORS['البلاتينية']};
        color: #333;
    }}
    
    .band-gold {{
        background-color: {BAND_COLORS['الذهبية']};
        color: #333;
    }}
    
    .band-silver {{
        background-color: {BAND_COLORS['الفضية']};
        color: #333;
    }}
    
    .band-bronze {{
        background-color: {BAND_COLORS['البرونزية']};
        color: white;
    }}
    
    .band-improvement {{
        background-color: {BAND_COLORS['يحتاج إلى تطوير']};
        color: white;
    }}
    
    .band-none {{
        background-color: {BAND_COLORS['لا يستفيد من النظام']};
        color: white;
    }}
    
    /* ============================================
       RESPONSIVE DESIGN
       ============================================ */
    
    @media (max-width: 768px) {{
        .professional-header h1 {{
            font-size: 2rem;
        }}
        
        .professional-header .subtitle {{
            font-size: 1rem;
        }}
        
        .metric-card .value {{
            font-size: 2rem;
        }}
    }}
    
    /* ============================================
       SCROLLBAR
       ============================================ */
    
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: #f1f1f1;
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {QATAR_MAROON};
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {QATAR_GOLD};
    }}
    
    /* ============================================
       LOADING SPINNER
       ============================================ */
    
    .stSpinner > div {{
        border-top-color: {QATAR_MAROON} !important;
    }}
    
    </style>
    """
    
    return css


def get_header_html(logo_horizontal_path=None):
    """
    Get professional header HTML.
    
    Args:
        logo_horizontal_path: Path to horizontal logo
    
    Returns:
        str: HTML code
    """
    
    logo_html = ""
    if logo_horizontal_path:
        logo_html = f'<img src="{logo_horizontal_path}" alt="إنجاز" />'
    
    html = f"""
    <div class="professional-header">
        <div class="header-content" style="display: flex; align-items: center; justify-content: center; gap: 1.5rem; flex-wrap: wrap;">
            <div class="logo-side" style="flex-shrink: 0;">
                {logo_html}
            </div>
            <div class="text-side" style="text-align: right;">
                <h1 style="margin: 0; font-size: 2rem; font-weight: 800;">إنجاز - نظام تحليل التقييمات الإلكترونية الأسبوعية</h1>
                <div class="subtitle" style="margin-top: 0.5rem; font-size: 1.2rem; font-weight: 600;">تنمية رقمية مستدامة</div>
                <div class="tagline" style="margin-top: 0.3rem; font-size: 1rem; font-weight: 500;">قطر للتعليم</div>
            </div>
        </div>
    </div>
    """
    
    return html


def get_footer_html():
    """
    Get professional footer HTML.
    
    Returns:
        str: HTML code
    """
    
    html = """
    <div class="professional-footer">
        <h3>🎯 رؤيتنا</h3>
        <p><strong>"متعلم ريادي لتنمية مستدامة"</strong></p>
        <div class="divider"></div>
        <p>
            <strong>منسق المشاريع الإلكترونية:</strong> سحر عثمان<br>
            <strong>البريد الإلكتروني:</strong> <a href="mailto:Sahar.Osman@education.qa">Sahar.Osman@education.qa</a>
        </p>
        <div class="divider"></div>
        <p>
            مدرسة عثمان بن عفّان النموذجية للبنين<br>
            وزارة التعليم والتعليم العالي - دولة قطر 🇶🇦
        </p>
        <p style="margin-top: 1.5rem; font-size: 0.9rem; opacity: 0.8;">
            © 2025 — جميع الحقوق محفوظة | Made with ❤️ in Qatar
        </p>
    </div>
    """
    
    return html


def get_metric_card_html(title, value, subtitle, badge=None):
    """
    Get metric card HTML.
    
    Args:
        title: Card title
        value: Main value
        subtitle: Subtitle text
        badge: Optional badge text
    
    Returns:
        str: HTML code
    """
    
    badge_html = f'<div class="badge">{badge}</div>' if badge else ''
    
    html = f"""
    <div class="metric-card">
        <h3>{title}</h3>
        <div class="value">{value}</div>
        <div class="subtitle">{subtitle}</div>
        {badge_html}
    </div>
    """
    
    return html

