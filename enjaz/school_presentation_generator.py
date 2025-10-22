"""
Module for generating school-level presentation with coordinator actions.
"""

import os
import tempfile
from datetime import datetime


def generate_coordinator_actions_slide_html(actions_text, school_stats):
    """
    Generate HTML for coordinator actions slide.
    
    Args:
        actions_text: Text containing coordinator actions
        school_stats: Dictionary with school statistics
    
    Returns:
        HTML string for the slide
    """
    
    # Format actions text for HTML (preserve line breaks)
    formatted_actions = actions_text.replace('\n', '<br>')
    
    completion_rate = school_stats.get('completion_rate', 0.0)
    total_students = school_stats.get('total_students', 0)
    
    html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>إجراءات منسق المشاريع</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
        }}
        .slide-container {{
            width: 1280px;
            min-height: 720px;
            background: #FFFFFF;
        }}
        .header {{
            background: linear-gradient(135deg, #8A1538 0%, #6d3a46 100%);
            padding: 30px 60px;
            color: white;
        }}
        .header h1 {{
            font-size: 44px;
            font-weight: 700;
            margin: 0;
        }}
        .header-subtitle {{
            font-size: 22px;
            margin-top: 10px;
            color: #D4AF37;
        }}
        .content {{
            padding: 30px 80px;
        }}
        .stats-bar {{
            background: #f8f9fa;
            padding: 20px 30px;
            margin-bottom: 25px;
            border-right: 5px solid #8A1538;
            display: flex;
            justify-content: space-around;
            align-items: center;
        }}
        .stat-item {{
            text-align: center;
        }}
        .stat-value {{
            font-size: 32px;
            font-weight: 700;
            color: #8A1538;
        }}
        .stat-label {{
            font-size: 16px;
            color: #666;
            margin-top: 5px;
        }}
        .actions-content {{
            background: #ffffff;
            padding: 25px 35px;
            border: 2px solid #8A1538;
            min-height: 450px;
            font-size: 19px;
            line-height: 1.8;
            color: #333;
        }}
        .actions-content strong {{
            color: #8A1538;
        }}
    </style>
</head>
<body>
    <div class="slide-container">
        <div class="header">
            <h1>📋 إجراءات منسق المشاريع</h1>
            <div class="header-subtitle">التقرير الكمي الوصفي - مستوى المدرسة</div>
        </div>
        
        <div class="content">
            <div class="stats-bar">
                <div class="stat-item">
                    <div class="stat-value">{total_students}</div>
                    <div class="stat-label">إجمالي الطلاب</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{completion_rate:.1f}%</div>
                    <div class="stat-label">نسبة الإنجاز الكلية</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{datetime.now().strftime('%Y-%m-%d')}</div>
                    <div class="stat-label">تاريخ التقرير</div>
                </div>
            </div>
            
            <div class="actions-content">
                {formatted_actions}
            </div>
        </div>
    </div>
</body>
</html>"""
    
    return html_content


def save_coordinator_actions_slide(actions_text, school_stats, output_path):
    """
    Save coordinator actions as an HTML slide file.
    
    Args:
        actions_text: Text containing coordinator actions
        school_stats: Dictionary with school statistics
        output_path: Path where to save the HTML file
    
    Returns:
        Path to the saved HTML file
    """
    html_content = generate_coordinator_actions_slide_html(actions_text, school_stats)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_path

