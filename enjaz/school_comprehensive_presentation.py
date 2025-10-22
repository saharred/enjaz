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


def get_presentation_outline(school_stats, subject_stats, coordinator_recommendation="", coordinator_actions=""):
    """
    Generate presentation outline based on data.
    
    Args:
        school_stats: Dictionary with school statistics
        subject_stats: List of subject statistics
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
        'summary': 'عرض توزيع الطلاب على الفئات الستة مع الأعداد والنسب المئوية ورسم بياني',
        'image_plan': ''
    })
    
    # Slide 4: General Subject Analysis
    outline.append({
        'id': 'subject_overview',
        'page_title': 'التحليل العام للمواد',
        'summary': f'نظرة شاملة على أداء {len(subject_stats)} مادة دراسية مع المواد الأعلى والأقل أداءً',
        'image_plan': ''
    })
    
    # Slides 5-N: Individual subject analysis
    for idx, subject in enumerate(subject_stats, 1):
        outline.append({
            'id': f'subject_{idx}',
            'page_title': f'{subject["subject_name"]} - التحليل التفصيلي',
            'summary': f'تحليل تفصيلي لمادة {subject["subject_name"]}: نسبة إنجاز {subject["completion_rate"]:.1f}%، توزيع الفئات، والتوصيات',
            'image_plan': ''
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

