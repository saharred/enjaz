"""
Module for generating comprehensive school-level presentation.
Includes all analyses, subject details, band distribution, and coordinator inputs.
"""

import streamlit as st
from enjaz.analysis import get_band, get_band_emoji
from enjaz.department_recommendations import get_subject_recommendation
import pandas as pd


def calculate_subject_statistics(all_data):
    """
    Calculate statistics for each subject.
    
    Args:
        all_data: List of sheet data dictionaries
    
    Returns:
        List of dictionaries with subject statistics
    """
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
        
        # Calculate band distribution for this subject
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
        
        subject_stats.append({
            'subject_name': subject_name,
            'total_students': total_students,
            'total_due': total_due,
            'total_completed': total_completed,
            'completion_rate': completion_rate,
            'band': get_band(completion_rate),
            'band_counts': band_counts,
            'band_percentages': band_percentages,
            'recommendation': get_subject_recommendation(completion_rate)
        })
    
    # Sort by completion rate (descending)
    subject_stats.sort(key=lambda x: x['completion_rate'], reverse=True)
    
    return subject_stats


def calculate_school_statistics_for_presentation(all_data):
    """
    Calculate comprehensive school-level statistics for presentation.
    
    Args:
        all_data: List of sheet data dictionaries
    
    Returns:
        Dictionary with school statistics
    """
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
            'يحتاج إلى تطوير': 0,
            'لا يستفيد من النظام': 0
        }
    }
    
    if not all_data:
        return stats
    
    # Collect all unique students
    all_students = {}
    
    for sheet_data in all_data:
        for student in sheet_data['students']:
            if not student.get('has_due', False):
                continue
            
            student_name = student['student_name']
            
            if student_name not in all_students:
                all_students[student_name] = {
                    'total_due': 0,
                    'completed': 0
                }
            
            all_students[student_name]['total_due'] += student['total_due']
            all_students[student_name]['completed'] += student['completed']
    
    # Calculate stats
    stats['total_students'] = len(all_students)
    
    for student_data in all_students.values():
        stats['total_assessments'] += student_data['total_due']
        stats['total_completed'] += student_data['completed']
        
        # Calculate student's overall completion rate
        if student_data['total_due'] > 0:
            student_rate = (student_data['completed'] / student_data['total_due']) * 100
            band = get_band(student_rate)
            if band in stats['band_distribution']:
                stats['band_distribution'][band] += 1
    
    # Calculate overall completion rate
    if stats['total_assessments'] > 0:
        stats['completion_rate'] = (stats['total_completed'] / stats['total_assessments']) * 100
    
    return stats


def get_presentation_outline(school_stats, subject_stats, top_performers_stats, struggling_students_stats, coordinator_recommendation="", coordinator_actions=""):
    """
    Generate presentation outline based on data.
    
    Args:
        school_stats: Dictionary with school statistics
        subject_stats: List of subject statistics
        top_performers_stats: Dictionary with top performers statistics
        struggling_students_stats: Dictionary with struggling students statistics
        coordinator_recommendation: Text for coordinator's recommendation
        coordinator_actions: Text for coordinator's actions
    
    Returns:
        List of slide dictionaries for slide_initialize
    """
    outline = []
    
    # Slide 1: Title slide
    outline.append({
        'id': 'title',
        'page_title': 'تقرير المدرسة الشامل',
        'summary': 'الشريحة الافتتاحية للعرض التقديمي مع عنوان التقرير والمعلومات الأساسية',
        'image_plan': ''
    })
    
    # Slide 2: Overview - Key Statistics
    outline.append({
        'id': 'overview',
        'page_title': 'الإحصائيات الرئيسية',
        'summary': f'عرض الإحصائيات الرئيسية: {school_stats["total_students"]} طالب، {school_stats["total_assessments"]} تقييم، نسبة إنجاز {school_stats["completion_rate"]:.1f}%',
        'image_plan': ''
    })
    
    # Slide 3: Band Distribution
    outline.append({
        'id': 'band_distribution',
        'page_title': 'توزيع الطلاب حسب الفئات',
        'summary': 'عرض توزيع الطلاب على الفئات الستة مع الأعداد والنسب المئوية ورسم بياني دائري تفاعلي',
        'image_plan': '',
        'has_chart': True,
        'chart_type': 'band_distribution'
    })
    
    # Slide 4: General Subject Analysis
    outline.append({
        'id': 'subject_overview',
        'page_title': 'التحليل العام للمواد',
        'summary': f'نظرة شاملة على أداء {len(subject_stats)} مادة دراسية مع رسم بياني مقارن للمواد',
        'image_plan': '',
        'has_chart': True,
        'chart_type': 'subject_comparison'
    })
    
    # Slide 5: Top Performers Analysis
    if top_performers_stats['total_top_performers'] > 0:
        outline.append({
            'id': 'top_performers',
            'page_title': 'تحليل أداء الطلاب المتفوقين',
            'summary': f'عدد الطلاب المتفوقين: {top_performers_stats["total_top_performers"]} طالب ({top_performers_stats["percentage_of_total"]:.1f}% من الإجمالي)، مع تفاصيل البلاتينية والذهبية',
            'image_plan': '',
            'has_chart': True,
            'chart_type': 'top_performers',
            'top_performers_data': top_performers_stats
        })
    
    # Slide 6: Struggling Students Analysis
    if struggling_students_stats['total_struggling'] > 0:
        outline.append({
            'id': 'struggling_students',
            'page_title': 'تحليل أداء الطلاب المتعثرين',
            'summary': f'عدد الطلاب المتعثرين: {struggling_students_stats["total_struggling"]} طالب ({struggling_students_stats["percentage_of_total"]:.1f}% من الإجمالي)، مع توصيات للتدخل الفوري',
            'image_plan': '',
            'has_chart': True,
            'chart_type': 'struggling_students',
            'struggling_students_data': struggling_students_stats
        })
    
    # Slides 5-N: Individual subject analysis
    for idx, subject in enumerate(subject_stats, 1):
        outline.append({
            'id': f'subject_{idx}',
            'page_title': f'{subject["subject_name"]} - التحليل التفصيلي',
            'summary': f'تحليل تفصيلي لمادة {subject["subject_name"]}: نسبة إنجاز {subject["completion_rate"]:.1f}%، توزيع الفئات مع رسم بياني، والتوصيات',
            'image_plan': '',
            'has_chart': True,
            'chart_type': 'subject_band',
            'subject_data': subject
        })
    
    # Slide N+1: General Recommendations
    outline.append({
        'id': 'recommendations',
        'page_title': 'التوصيات العامة',
        'summary': f'توصيات بناءً على نسبة الإنجاز الكلية ({school_stats["completion_rate"]:.1f}%) واستراتيجيات التحسين المقترحة',
        'image_plan': ''
    })
    
    # Slide N+2: Coordinator Recommendation
    if coordinator_recommendation:
        outline.append({
            'id': 'coordinator_recommendation',
            'page_title': 'توصية منسق المشاريع',
            'summary': 'التوصية الخاصة من منسق المشاريع بناءً على التحليل الشامل',
            'image_plan': ''
        })
    
    # Slide N+3: Coordinator Actions
    if coordinator_actions:
        outline.append({
            'id': 'coordinator_actions',
            'page_title': 'إجراءات منسق المشاريع',
            'summary': 'الإجراءات المتخذة والمخطط لها من قبل منسق المشاريع لتحسين الأداء',
            'image_plan': ''
        })
    
    # Final slide: Closing
    outline.append({
        'id': 'closing',
        'page_title': 'شكراً لكم',
        'summary': 'الشريحة الختامية مع رؤية المدرسة ومعلومات الاتصال',
        'image_plan': ''
    })
    
    return outline





def generate_band_distribution_chart_html(band_distribution, total_students):
    """
    Generate HTML/JavaScript for band distribution pie chart using Chart.js.
    
    Args:
        band_distribution: Dictionary with band names and counts
        total_students: Total number of students
    
    Returns:
        HTML string with chart
    """
    # Prepare data
    labels = list(band_distribution.keys())
    data = list(band_distribution.values())
    
    # Colors for each band
    colors = [
        '#E5E4E2',  # البلاتينية - Platinum
        '#FFD700',  # الذهبية - Gold
        '#C0C0C0',  # الفضية - Silver
        '#CD7F32',  # البرونزية - Bronze
        '#FF6600',  # يحتاج إلى تطوير - Orange
        '#C00000'   # لا يستفيد من النظام - Red
    ]
    
    chart_html = f"""
    <div style="width: 100%; height: 400px; display: flex; justify-content: center; align-items: center;">
        <canvas id="bandChart"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <script>
    const ctx = document.getElementById('bandChart').getContext('2d');
    const bandChart = new Chart(ctx, {{
        type: 'doughnut',
        data: {{
            labels: {labels},
            datasets: [{{
                data: {data},
                backgroundColor: {colors},
                borderWidth: 2,
                borderColor: '#ffffff'
            }}]
        }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{
                    position: 'right',
                    rtl: true,
                    labels: {{
                        font: {{
                            family: 'Tajawal',
                            size: 16
                        }},
                        padding: 15,
                        usePointStyle: true
                    }}
                }},
                tooltip: {{
                    rtl: true,
                    callbacks: {{
                        label: function(context) {{
                            let label = context.label || '';
                            let value = context.parsed || 0;
                            let percentage = ((value / {total_students}) * 100).toFixed(1);
                            return label + ': ' + value + ' طالب (' + percentage + '%)';
                        }}
                    }}
                }}
            }}
        }}
    }});
    </script>
    """
    
    return chart_html


def generate_subject_comparison_chart_html(subject_stats):
    """
    Generate HTML/JavaScript for subject comparison bar chart using Chart.js.
    
    Args:
        subject_stats: List of subject statistics dictionaries
    
    Returns:
        HTML string with chart
    """
    # Prepare data (top 10 subjects by completion rate)
    top_subjects = subject_stats[:10]
    labels = [s['subject_name'] for s in top_subjects]
    data = [s['completion_rate'] for s in top_subjects]
    
    # Color based on completion rate
    colors = []
    for rate in data:
        if rate >= 90:
            colors.append('#E5E4E2')  # Platinum
        elif rate >= 80:
            colors.append('#FFD700')  # Gold
        elif rate >= 70:
            colors.append('#C0C0C0')  # Silver
        elif rate >= 50:
            colors.append('#CD7F32')  # Bronze
        elif rate >= 1:
            colors.append('#FF6600')  # Orange
        else:
            colors.append('#C00000')  # Red
    
    chart_html = f"""
    <div style="width: 100%; height: 400px;">
        <canvas id="subjectChart"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <script>
    const ctx2 = document.getElementById('subjectChart').getContext('2d');
    const subjectChart = new Chart(ctx2, {{
        type: 'bar',
        data: {{
            labels: {labels},
            datasets: [{{
                label: 'نسبة الإنجاز %',
                data: {data},
                backgroundColor: {colors},
                borderWidth: 0
            }}]
        }},
        options: {{
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{
                    display: false
                }},
                tooltip: {{
                    rtl: true,
                    callbacks: {{
                        label: function(context) {{
                            return 'نسبة الإنجاز: ' + context.parsed.x.toFixed(1) + '%';
                        }}
                    }}
                }}
            }},
            scales: {{
                x: {{
                    beginAtZero: true,
                    max: 100,
                    ticks: {{
                        font: {{
                            family: 'Tajawal',
                            size: 14
                        }}
                    }},
                    grid: {{
                        color: 'rgba(0, 0, 0, 0.05)'
                    }}
                }},
                y: {{
                    ticks: {{
                        font: {{
                            family: 'Tajawal',
                            size: 14
                        }}
                    }},
                    grid: {{
                        display: false
                    }}
                }}
            }}
        }}
    }});
    </script>
    """
    
    return chart_html


def generate_subject_band_chart_html(band_counts, subject_name):
    """
    Generate HTML/JavaScript for individual subject band distribution chart.
    
    Args:
        band_counts: Dictionary with band names and counts for this subject
        subject_name: Name of the subject
    
    Returns:
        HTML string with chart
    """
    labels = list(band_counts.keys())
    data = list(band_counts.values())
    
    colors = [
        '#E5E4E2',  # البلاتينية
        '#FFD700',  # الذهبية
        '#C0C0C0',  # الفضية
        '#CD7F32',  # البرونزية
        '#FF6600',  # يحتاج إلى تطوير
        '#C00000'   # لا يستفيد من النظام
    ]
    
    chart_html = f"""
    <div style="width: 100%; height: 300px;">
        <canvas id="subjectBandChart_{subject_name.replace(' ', '_')}"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <script>
    const ctx3 = document.getElementById('subjectBandChart_{subject_name.replace(' ', '_')}').getContext('2d');
    const chart = new Chart(ctx3, {{
        type: 'bar',
        data: {{
            labels: {labels},
            datasets: [{{
                label: 'عدد الطلاب',
                data: {data},
                backgroundColor: {colors},
                borderWidth: 0
            }}]
        }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{
                    display: false
                }},
                tooltip: {{
                    rtl: true,
                    callbacks: {{
                        label: function(context) {{
                            return 'عدد الطلاب: ' + context.parsed.y;
                        }}
                    }}
                }}
            }},
            scales: {{
                x: {{
                    ticks: {{
                        font: {{
                            family: 'Tajawal',
                            size: 12
                        }}
                    }},
                    grid: {{
                        display: false
                    }}
                }},
                y: {{
                    beginAtZero: true,
                    ticks: {{
                        stepSize: 1,
                        font: {{
                            family: 'Tajawal',
                            size: 12
                        }}
                    }},
                    grid: {{
                        color: 'rgba(0, 0, 0, 0.05)'
                    }}
                }}
            }}
        }}
    }});
    </script>
    """
    
    return chart_html





def calculate_top_performers_statistics(all_data):
    """
    Calculate statistics for top performing students (Platinum and Gold bands).
    
    Args:
        all_data: List of sheet data dictionaries
    
    Returns:
        Dictionary with top performers statistics
    """
    stats = {
        'total_top_performers': 0,
        'platinum_count': 0,
        'gold_count': 0,
        'percentage_of_total': 0.0,
        'top_students': [],  # List of student names and their rates
        'subjects_excellence': {}  # Subject-wise top performers count
    }
    
    if not all_data:
        return stats
    
    # Collect all unique students with their overall performance
    all_students = {}
    
    for sheet_data in all_data:
        subject_name = sheet_data.get('subject', sheet_data['sheet_name'])
        
        for student in sheet_data['students']:
            if not student.get('has_due', False):
                continue
            
            student_name = student['student_name']
            
            if student_name not in all_students:
                all_students[student_name] = {
                    'total_due': 0,
                    'completed': 0,
                    'subjects': []
                }
            
            all_students[student_name]['total_due'] += student['total_due']
            all_students[student_name]['completed'] += student['completed']
            all_students[student_name]['subjects'].append({
                'subject': subject_name,
                'rate': student['completion_rate']
            })
    
    # Calculate overall rates and identify top performers
    top_students_list = []
    
    for student_name, student_data in all_students.items():
        if student_data['total_due'] > 0:
            overall_rate = (student_data['completed'] / student_data['total_due']) * 100
            band = get_band(overall_rate)
            
            if band in ['البلاتينية', 'الذهبية']:
                stats['total_top_performers'] += 1
                
                if band == 'البلاتينية':
                    stats['platinum_count'] += 1
                else:
                    stats['gold_count'] += 1
                
                top_students_list.append({
                    'name': student_name,
                    'rate': overall_rate,
                    'band': band,
                    'subjects': student_data['subjects']
                })
                
                # Count subject-wise excellence
                for subject_info in student_data['subjects']:
                    if subject_info['rate'] >= 80:  # Gold or Platinum in this subject
                        subject = subject_info['subject']
                        if subject not in stats['subjects_excellence']:
                            stats['subjects_excellence'][subject] = 0
                        stats['subjects_excellence'][subject] += 1
    
    # Sort top students by rate (descending)
    top_students_list.sort(key=lambda x: x['rate'], reverse=True)
    stats['top_students'] = top_students_list
    
    # Calculate percentage
    total_students = len(all_students)
    if total_students > 0:
        stats['percentage_of_total'] = (stats['total_top_performers'] / total_students) * 100
    
    return stats


def generate_top_performers_chart_html(platinum_count, gold_count):
    """
    Generate HTML/JavaScript for top performers comparison chart.
    
    Args:
        platinum_count: Number of platinum students
        gold_count: Number of gold students
    
    Returns:
        HTML string with chart
    """
    chart_html = f"""
    <div style="width: 100%; height: 350px;">
        <canvas id="topPerformersChart"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <script>
    const ctx = document.getElementById('topPerformersChart').getContext('2d');
    const chart = new Chart(ctx, {{
        type: 'bar',
        data: {{
            labels: ['البلاتينية 💎', 'الذهبية 🥇'],
            datasets: [{{
                label: 'عدد الطلاب المتفوقين',
                data: [{platinum_count}, {gold_count}],
                backgroundColor: ['#E5E4E2', '#FFD700'],
                borderWidth: 0
            }}]
        }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{
                    display: false
                }},
                tooltip: {{
                    rtl: true,
                    callbacks: {{
                        label: function(context) {{
                            return 'عدد الطلاب: ' + context.parsed.y;
                        }}
                    }}
                }}
            }},
            scales: {{
                x: {{
                    ticks: {{
                        font: {{
                            family: 'Tajawal',
                            size: 16
                        }}
                    }},
                    grid: {{
                        display: false
                    }}
                }},
                y: {{
                    beginAtZero: true,
                    ticks: {{
                        stepSize: 1,
                        font: {{
                            family: 'Tajawal',
                            size: 14
                        }}
                    }},
                    grid: {{
                        color: 'rgba(0, 0, 0, 0.05)'
                    }}
                }}
            }}
        }}
    }});
    </script>
    """
    
    return chart_html





def calculate_struggling_students_statistics(all_data):
    """
    Calculate statistics for struggling students (Needs Development and Not Benefiting bands).
    
    Args:
        all_data: List of sheet data dictionaries
    
    Returns:
        Dictionary with struggling students statistics
    """
    stats = {
        'total_struggling': 0,
        'needs_development_count': 0,  # 1-49.99%
        'not_benefiting_count': 0,      # 0%
        'percentage_of_total': 0.0,
        'struggling_students': [],  # List of student names and their rates
        'subjects_concern': {},  # Subject-wise struggling students count
        'intervention_priority': []  # Students who need immediate intervention
    }
    
    if not all_data:
        return stats
    
    # Collect all unique students with their overall performance
    all_students = {}
    
    for sheet_data in all_data:
        subject_name = sheet_data.get('subject', sheet_data['sheet_name'])
        
        for student in sheet_data['students']:
            if not student.get('has_due', False):
                continue
            
            student_name = student['student_name']
            
            if student_name not in all_students:
                all_students[student_name] = {
                    'total_due': 0,
                    'completed': 0,
                    'subjects': []
                }
            
            all_students[student_name]['total_due'] += student['total_due']
            all_students[student_name]['completed'] += student['completed']
            all_students[student_name]['subjects'].append({
                'subject': subject_name,
                'rate': student['completion_rate']
            })
    
    # Calculate overall rates and identify struggling students
    struggling_students_list = []
    
    for student_name, student_data in all_students.items():
        if student_data['total_due'] > 0:
            overall_rate = (student_data['completed'] / student_data['total_due']) * 100
            band = get_band(overall_rate)
            
            if band in ['يحتاج إلى تطوير', 'لا يستفيد من النظام']:
                stats['total_struggling'] += 1
                
                if band == 'يحتاج إلى تطوير':
                    stats['needs_development_count'] += 1
                else:
                    stats['not_benefiting_count'] += 1
                
                struggling_students_list.append({
                    'name': student_name,
                    'rate': overall_rate,
                    'band': band,
                    'subjects': student_data['subjects']
                })
                
                # Count subject-wise struggling
                for subject_info in student_data['subjects']:
                    if subject_info['rate'] < 50:  # Struggling in this subject
                        subject = subject_info['subject']
                        if subject not in stats['subjects_concern']:
                            stats['subjects_concern'][subject] = 0
                        stats['subjects_concern'][subject] += 1
                
                # Identify students who need immediate intervention (0% or very low)
                if overall_rate < 10:
                    stats['intervention_priority'].append({
                        'name': student_name,
                        'rate': overall_rate
                    })
    
    # Sort struggling students by rate (ascending - worst first)
    struggling_students_list.sort(key=lambda x: x['rate'])
    stats['struggling_students'] = struggling_students_list
    
    # Calculate percentage
    total_students = len(all_students)
    if total_students > 0:
        stats['percentage_of_total'] = (stats['total_struggling'] / total_students) * 100
    
    return stats


def generate_struggling_students_chart_html(needs_development_count, not_benefiting_count):
    """
    Generate HTML/JavaScript for struggling students comparison chart.
    
    Args:
        needs_development_count: Number of students who need development
        not_benefiting_count: Number of students not benefiting
    
    Returns:
        HTML string with chart
    """
    chart_html = f"""
    <div style="width: 100%; height: 350px;">
        <canvas id="strugglingStudentsChart"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <script>
    const ctx = document.getElementById('strugglingStudentsChart').getContext('2d');
    const chart = new Chart(ctx, {{
        type: 'bar',
        data: {{
            labels: ['يحتاج إلى تطوير ⚠️', 'لا يستفيد من النظام ❌'],
            datasets: [{{
                label: 'عدد الطلاب المتعثرين',
                data: [{needs_development_count}, {not_benefiting_count}],
                backgroundColor: ['#FF6600', '#C00000'],
                borderWidth: 0
            }}]
        }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{
                    display: false
                }},
                tooltip: {{
                    rtl: true,
                    callbacks: {{
                        label: function(context) {{
                            return 'عدد الطلاب: ' + context.parsed.y;
                        }}
                    }}
                }}
            }},
            scales: {{
                x: {{
                    ticks: {{
                        font: {{
                            family: 'Tajawal',
                            size: 16
                        }}
                    }},
                    grid: {{
                        display: false
                    }}
                }},
                y: {{
                    beginAtZero: true,
                    ticks: {{
                        stepSize: 1,
                        font: {{
                            family: 'Tajawal',
                            size: 14
                        }}
                    }},
                    grid: {{
                        color: 'rgba(0, 0, 0, 0.05)'
                    }}
                }}
            }}
        }}
    }});
    </script>
    """
    
    return chart_html

