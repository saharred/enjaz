"""
Advanced Charts Module for Enjaz Application.
Creates interactive and professional charts using Plotly.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

# Qatar brand colors
QATAR_MAROON = "#8A1538"
QATAR_GOLD = "#C9A227"

# Band colors
BAND_COLORS = {
    "ممتاز جداً": "#2ECC71",  # Green
    "جيد جداً": "#3498DB",     # Blue
    "جيد": "#F39C12",          # Orange
    "يحتاج إلى تحسين": "#E67E22",  # Dark Orange
    "ضعيف": "#E74C3C",        # Red
    "انعدام الإنجاز": "#95A5A6"  # Gray
}


def create_band_distribution_chart(all_data, title="توزيع الطلاب حسب الفئات"):
    """
    Create pie chart showing distribution of students across performance bands.
    
    Args:
        all_data: List of sheet data
        title: Chart title
    
    Returns:
        plotly.graph_objects.Figure
    """
    from enjaz.analysis import get_band
    
    # Count students in each band
    band_counts = {
        "ممتاز جداً": 0,
        "جيد جداً": 0,
        "جيد": 0,
        "يحتاج إلى تحسين": 0,
        "ضعيف": 0,
        "انعدام الإنجاز": 0
    }
    
    for sheet_data in all_data:
        for student in sheet_data['students']:
            if student['has_due']:
                band = get_band(student['completion_rate'])
                band_counts[band] += 1
    
    # Filter out zero counts
    labels = [k for k, v in band_counts.items() if v > 0]
    values = [v for v in band_counts.values() if v > 0]
    colors = [BAND_COLORS[label] for label in labels]
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textinfo='label+percent+value',
        textfont=dict(size=14, family='Arial, sans-serif'),
        hole=0.3  # Donut chart
    )])
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color=QATAR_MAROON, family='Arial, sans-serif'),
            x=0.5,
            xanchor='center'
        ),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=12, family='Arial, sans-serif')
        ),
        height=500
    )
    
    return fig


def create_class_comparison_chart(all_data, title="مقارنة الشعب"):
    """
    Create bar chart comparing performance across classes/sections.
    
    Args:
        all_data: List of sheet data
        title: Chart title
    
    Returns:
        plotly.graph_objects.Figure
    """
    # Aggregate by class
    class_stats = {}
    
    for sheet_data in all_data:
        class_code = sheet_data.get('class_code', 'Unknown')
        
        students_with_due = [s for s in sheet_data['students'] if s['has_due']]
        
        if not students_with_due:
            continue
        
        if class_code not in class_stats:
            class_stats[class_code] = {
                'total_students': 0,
                'total_completion': 0
            }
        
        class_stats[class_code]['total_students'] += len(students_with_due)
        class_stats[class_code]['total_completion'] += sum(s['completion_rate'] for s in students_with_due)
    
    # Calculate averages
    classes = []
    avg_completions = []
    
    for class_code, stats in class_stats.items():
        if stats['total_students'] > 0:
            classes.append(class_code)
            avg_completions.append(stats['total_completion'] / stats['total_students'])
    
    # Sort by completion rate
    sorted_data = sorted(zip(classes, avg_completions), key=lambda x: x[1], reverse=True)
    classes, avg_completions = zip(*sorted_data) if sorted_data else ([], [])
    
    # Create bar chart
    fig = go.Figure(data=[go.Bar(
        x=list(classes),
        y=list(avg_completions),
        marker=dict(
            color=list(avg_completions),
            colorscale=[[0, '#E74C3C'], [0.5, '#F39C12'], [1, '#2ECC71']],
            showscale=True,
            colorbar=dict(title="نسبة الإنجاز %")
        ),
        text=[f"{v:.1f}%" for v in avg_completions],
        textposition='outside',
        textfont=dict(size=12, family='Arial, sans-serif')
    )])
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color=QATAR_MAROON, family='Arial, sans-serif'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="الشعبة",
            titlefont=dict(size=14, family='Arial, sans-serif'),
            tickfont=dict(size=12, family='Arial, sans-serif')
        ),
        yaxis=dict(
            title="متوسط نسبة الإنجاز (%)",
            titlefont=dict(size=14, family='Arial, sans-serif'),
            tickfont=dict(size=12, family='Arial, sans-serif'),
            range=[0, 100]
        ),
        height=500,
        showlegend=False
    )
    
    return fig


def create_subject_comparison_chart(all_data, title="مقارنة المواد"):
    """
    Create bar chart comparing performance across subjects.
    
    Args:
        all_data: List of sheet data
        title: Chart title
    
    Returns:
        plotly.graph_objects.Figure
    """
    # Aggregate by subject
    subject_stats = {}
    
    for sheet_data in all_data:
        subject = sheet_data.get('subject', sheet_data['sheet_name'])
        
        students_with_due = [s for s in sheet_data['students'] if s['has_due']]
        
        if not students_with_due:
            continue
        
        if subject not in subject_stats:
            subject_stats[subject] = {
                'total_students': 0,
                'total_completion': 0
            }
        
        subject_stats[subject]['total_students'] += len(students_with_due)
        subject_stats[subject]['total_completion'] += sum(s['completion_rate'] for s in students_with_due)
    
    # Calculate averages
    subjects = []
    avg_completions = []
    
    for subject, stats in subject_stats.items():
        if stats['total_students'] > 0:
            subjects.append(subject)
            avg_completions.append(stats['total_completion'] / stats['total_students'])
    
    # Sort by completion rate
    sorted_data = sorted(zip(subjects, avg_completions), key=lambda x: x[1], reverse=True)
    subjects, avg_completions = zip(*sorted_data) if sorted_data else ([], [])
    
    # Create bar chart
    fig = go.Figure(data=[go.Bar(
        x=list(subjects),
        y=list(avg_completions),
        marker=dict(
            color=QATAR_MAROON,
            line=dict(color=QATAR_GOLD, width=2)
        ),
        text=[f"{v:.1f}%" for v in avg_completions],
        textposition='outside',
        textfont=dict(size=12, family='Arial, sans-serif')
    )])
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color=QATAR_MAROON, family='Arial, sans-serif'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="المادة",
            titlefont=dict(size=14, family='Arial, sans-serif'),
            tickfont=dict(size=12, family='Arial, sans-serif')
        ),
        yaxis=dict(
            title="متوسط نسبة الإنجاز (%)",
            titlefont=dict(size=14, family='Arial, sans-serif'),
            tickfont=dict(size=12, family='Arial, sans-serif'),
            range=[0, 100]
        ),
        height=500,
        showlegend=False
    )
    
    return fig


def create_student_performance_chart(student_data, student_name):
    """
    Create radar chart for individual student performance across subjects.
    
    Args:
        student_data: List of dicts with subject performance data
        student_name: Student name
    
    Returns:
        plotly.graph_objects.Figure
    """
    subjects = [d['subject'] for d in student_data]
    completion_rates = [d['completion_rate'] for d in student_data]
    
    # Add first point again to close the radar chart
    subjects_closed = subjects + [subjects[0]]
    completion_rates_closed = completion_rates + [completion_rates[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=completion_rates_closed,
        theta=subjects_closed,
        fill='toself',
        fillcolor='rgba(138, 21, 56, 0.3)',
        line=dict(color=QATAR_MAROON, width=2),
        marker=dict(color=QATAR_GOLD, size=8),
        name=student_name
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=12, family='Arial, sans-serif')
            ),
            angularaxis=dict(
                tickfont=dict(size=12, family='Arial, sans-serif')
            )
        ),
        title=dict(
            text=f"أداء الطالب: {student_name}",
            font=dict(size=18, color=QATAR_MAROON, family='Arial, sans-serif'),
            x=0.5,
            xanchor='center'
        ),
        showlegend=False,
        height=500
    )
    
    return fig


def create_comprehensive_dashboard(all_data):
    """
    Create comprehensive dashboard with multiple charts.
    
    Args:
        all_data: List of sheet data
    
    Returns:
        plotly.graph_objects.Figure
    """
    from enjaz.analysis import get_band
    
    # Calculate overall statistics
    total_students = 0
    total_completion = 0
    band_counts = {band: 0 for band in BAND_COLORS.keys()}
    
    for sheet_data in all_data:
        students_with_due = [s for s in sheet_data['students'] if s['has_due']]
        total_students += len(students_with_due)
        
        for student in students_with_due:
            total_completion += student['completion_rate']
            band = get_band(student['completion_rate'])
            band_counts[band] += 1
    
    avg_completion = total_completion / total_students if total_students > 0 else 0
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "توزيع الطلاب حسب الفئات",
            "مقارنة المواد",
            "مقارنة الشعب",
            "الإحصائيات العامة"
        ),
        specs=[
            [{"type": "pie"}, {"type": "bar"}],
            [{"type": "bar"}, {"type": "indicator"}]
        ]
    )
    
    # 1. Band distribution (pie chart)
    labels = [k for k, v in band_counts.items() if v > 0]
    values = [v for v in band_counts.values() if v > 0]
    colors = [BAND_COLORS[label] for label in labels]
    
    fig.add_trace(
        go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            textinfo='label+percent',
            hole=0.3
        ),
        row=1, col=1
    )
    
    # 2. Subject comparison
    subject_stats = {}
    for sheet_data in all_data:
        subject = sheet_data.get('subject', sheet_data['sheet_name'])
        students_with_due = [s for s in sheet_data['students'] if s['has_due']]
        
        if not students_with_due:
            continue
        
        if subject not in subject_stats:
            subject_stats[subject] = {'total': 0, 'count': 0}
        
        subject_stats[subject]['total'] += sum(s['completion_rate'] for s in students_with_due)
        subject_stats[subject]['count'] += len(students_with_due)
    
    subjects = list(subject_stats.keys())
    subject_avgs = [subject_stats[s]['total'] / subject_stats[s]['count'] for s in subjects]
    
    fig.add_trace(
        go.Bar(
            x=subjects,
            y=subject_avgs,
            marker=dict(color=QATAR_MAROON),
            text=[f"{v:.1f}%" for v in subject_avgs],
            textposition='outside'
        ),
        row=1, col=2
    )
    
    # 3. Class comparison
    class_stats = {}
    for sheet_data in all_data:
        class_code = sheet_data.get('class_code', 'Unknown')
        students_with_due = [s for s in sheet_data['students'] if s['has_due']]
        
        if not students_with_due:
            continue
        
        if class_code not in class_stats:
            class_stats[class_code] = {'total': 0, 'count': 0}
        
        class_stats[class_code]['total'] += sum(s['completion_rate'] for s in students_with_due)
        class_stats[class_code]['count'] += len(students_with_due)
    
    classes = list(class_stats.keys())
    class_avgs = [class_stats[c]['total'] / class_stats[c]['count'] for c in classes]
    
    fig.add_trace(
        go.Bar(
            x=classes,
            y=class_avgs,
            marker=dict(color=QATAR_GOLD),
            text=[f"{v:.1f}%" for v in class_avgs],
            textposition='outside'
        ),
        row=2, col=1
    )
    
    # 4. Overall indicator
    fig.add_trace(
        go.Indicator(
            mode="gauge+number+delta",
            value=avg_completion,
            title={'text': "متوسط الإنجاز العام"},
            delta={'reference': 75},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': QATAR_MAROON},
                'steps': [
                    {'range': [0, 40], 'color': "lightgray"},
                    {'range': [40, 60], 'color': "lightyellow"},
                    {'range': [60, 75], 'color': "lightblue"},
                    {'range': [75, 90], 'color': "lightgreen"},
                    {'range': [90, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': QATAR_GOLD, 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text="لوحة المعلومات الشاملة - نظام إنجاز",
            font=dict(size=20, color=QATAR_MAROON, family='Arial, sans-serif'),
            x=0.5,
            xanchor='center'
        ),
        showlegend=False,
        height=800
    )
    
    return fig

