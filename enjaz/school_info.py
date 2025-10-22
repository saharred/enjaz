"""
School information management module.
Handles school administrative data and configuration.
"""

import json
import os
from pathlib import Path


# Default school information
DEFAULT_SCHOOL_INFO = {
    'school_name': 'مدرسة عثمان بن عفان النموذجية للبنين',
    'school_name_en': 'Othman Bin Affan Model School for Boys',
    'projects_coordinator': 'سحر عثمان',
    'projects_coordinator_en': 'Sahar Osman',
    'academic_deputy': 'مريم القضع',
    'academic_deputy_en': 'Maryam Al-Qada',
    'admin_deputy': 'دلال الفهيدة',
    'admin_deputy_en': 'Dalal Al-Fuhaida',
    'principal': 'منيرة الهاجري',
    'principal_en': 'Munira Al-Hajri',
    'email': 'Sahar.Osman@education.qa',
    'vision': 'متعلم ريادي لتنمية مستدامة',
    'vision_en': 'Entrepreneurial learner for sustainable development'
}


def get_config_path():
    """Get path to school info configuration file."""
    return Path.home() / '.enjaz' / 'school_info.json'


def load_school_info():
    """
    Load school information from config file.
    If not exists, return default values.
    
    Returns:
        dict: School information
    """
    config_path = get_config_path()
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    
    return DEFAULT_SCHOOL_INFO.copy()


def save_school_info(school_info):
    """
    Save school information to config file.
    
    Args:
        school_info: dict with school information
    """
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(school_info, f, ensure_ascii=False, indent=2)


def update_school_info(**kwargs):
    """
    Update school information.
    
    Args:
        **kwargs: Fields to update
    
    Returns:
        dict: Updated school information
    """
    school_info = load_school_info()
    school_info.update(kwargs)
    save_school_info(school_info)
    return school_info


def get_qr_links():
    """
    Get QR code links for the report.
    
    Returns:
        dict: QR code links
    """
    return {
        'lms_link': 'https://lms.education.qa',
        'password_recovery': 'https://lms.education.qa/password-recovery',
        'qatar_tv': 'https://www.youtube.com/c/QatarEducationTV'
    }

