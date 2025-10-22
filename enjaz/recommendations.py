"""
Recommendations module for Enjaz application.
Generates Arabic professional recommendations for teachers.
"""


# Fixed reminder line to be included in all recommendations
FIXED_REMINDER = "تذكير الطلاب دائماً بحل التقييمات بنهاية كل حصة، ورقمنة استراتيجية الصفوف المقلوبة بتوظيف نظام قطر للتعليم."

# Parent communication reminder
PARENT_COMMUNICATION = "التواصل مع أولياء الأمور"


def get_band_from_percentage(percentage):
    """
    Get band based on completion percentage with new ranges.
    
    التصنيفات:
    - 🏆 البلاتينية (Platinum): 90% - 100%
    - 🥇 الذهبية (Gold): 75% - 89.99%
    - 🥈 الفضية (Silver): 60% - 74.99%
    - 🥉 البرونزية (Bronze): 40% - 59.99%
    - ⚠️ يحتاج إلى تحسين: 0.01% - 39.99%
    - ⭕ غير مستفيد: 0%
    
    Args:
        percentage: Completion percentage (0-100) or None
    
    Returns:
        str: Band name
    """
    if percentage is None:
        return "N/A"
    
    if percentage >= 90:
        return "البلاتينية"
    elif percentage >= 75:
        return "الذهبية"
    elif percentage >= 60:
        return "الفضية"
    elif percentage >= 40:
        return "البرونزية"
    elif percentage > 0:
        return "يحتاج إلى تحسين"
    else:
        return "غير مستفيد"


def get_band_color_new(band):
    """
    Get color for each band (new system).
    
    Args:
        band: Band name
    
    Returns:
        str: Hex color code
    """
    colors = {
        "البلاتينية": "#E5E4E2",      # Platinum
        "الذهبية": "#FFD700",        # Gold
        "الفضية": "#C0C0C0",        # Silver
        "البرونزية": "#CD7F32",    # Bronze
        "يحتاج إلى تحسين": "#FF6600", # Orange
        "غير مستفيد": "#C00000",  # Red
        "N/A": "#CCCCCC"
    }
    return colors.get(band, "#000000")


def get_band_emoji(band):
    """
    Get emoji for each band.
    
    Args:
        band: Band name
    
    Returns:
        str: Emoji
    """
    emojis = {
        "البلاتينية": "🏆",
        "الذهبية": "🥇",
        "الفضية": "🥈",
        "البرونزية": "🥉",
        "يحتاج إلى تحسين": "⚠️",
        "غير مستفيد": "⭕",
        "N/A": "➡️"
    }
    return emojis.get(band, "")


def get_class_recommendation_by_percentage(percentage, class_name):
    """
    Generate recommendation for class based on completion percentage.
    
    Args:
        percentage: Average completion percentage for the class
        class_name: Name of the class/subject
    
    Returns:
        str: Arabic recommendation text
    """
    if percentage is None:
        return f"لا توجد بيانات كافية لتقييم أداء {class_name}."
    
    band = get_band_from_percentage(percentage)
    emoji = get_band_emoji(band)
    
    recommendations = {
        "البلاتينية": f'{emoji} **نسبة الحل {percentage:.1f}% (البلاتينية)**\n\n"أظهر طلاب الصف التزامًا عاليًا بإنجاز التقييمات الأسبوعية على نظام قطر للتعليم بنسبة تفوق 90%. نوصي بالاستمرار على هذا النهج مع {FIXED_REMINDER}"',
        
        "الذهبية": f'{emoji} **نسبة الحل {percentage:.1f}% (الذهبية)**\n\n"حقق الصف مستوى ذهبي في حل التقييمات الأسبوعية. نقترح تعزيز هذا الأداء عبر {FIXED_REMINDER}"',
        
        "الفضية": f'{emoji} **نسبة الحل {percentage:.1f}% (الفضية)**\n\n"بلغ الصف نسبة إنجاز فضية في التقيييمات الأسبوعية (60–75%). نوصي بتكثيف {FIXED_REMINDER}"',
        
        "البرونزية": f'{emoji} **نسبة الحل {percentage:.1f}% (البرونزية)**\n\n"حقق الصف مستوى برونزي في حل التقييمات (40-60%). نوصي بالتركيز على تذكير الطلاب يوميًا في نهاية كل حصة بأهمية حل التقييمات، مع دمج استراتيجيات التعلم النشط ورقمنة الصفوف المقلوبة."',
        
        "يحتاج إلى تحسين": f'{emoji} **نسبة الحل {percentage:.1f}% (يحتاج إلى تحسين)**\n\n"نسبة الحل ما زالت تحتاج إلى تحسين عاجل، إذ لم تتجاوز 40%. نوصي بتكثيف الجهود عبر التذكير المستمر بنهاية الحصص بإنجاز التقييمات، مع {PARENT_COMMUNICATION}."',
        
        "غير مستفيد": f'{emoji} **نسبة الحل {percentage:.1f}% (غير مستفيد)**\n\n"لم ينجز الصف أي تقييم أسبوعي في هذه المادة. نوصي بإطلاق خطة عاجلة تشمل: تذكير الطلاب بنهاية كل حصة بأهمية إنجاز التقييمات، و{PARENT_COMMUNICATION}، مع اعتماد نظام قطر للتعليم كمنصة رئيسية."'
    }
    
    return recommendations.get(band, f"نسبة الحل: {percentage:.1f}%")


def get_subject_recommendation_by_percentage(percentage, subject_name):
    """
    Generate recommendation for subject based on completion percentage.
    
    Args:
        percentage: Average completion percentage for the subject
        subject_name: Name of the subject
    
    Returns:
        str: Arabic recommendation text
    """
    if percentage is None:
        return f"لا توجد بيانات كافية لتقييم أداء مادة {subject_name}."
    
    band = get_band_from_percentage(percentage)
    emoji = get_band_emoji(band)
    
    recommendations = {
        "البلاتينية": f'{emoji} **نسبة الحل {percentage:.1f}% (البلاتينية)**\n\n"المادة حققت نسبة إنجاز بلاتينية في التقييمات الأسبوعية على نظام قطر للتعليم. يُوصى بدعم استدامة هذا المستوى عبر توثيق أفضل الممارسات وتعميمها، مع {FIXED_REMINDER}"',
        
        "الذهبية": f'{emoji} **نسبة الحل {percentage:.1f}% (الذهبية)**\n\n"المادة أظهرت نسبة إنجاز ذهبية مع فرصة للارتقاء إلى مستوى البلاتينية. يُوصى بزيادة التحفيز والمتابعة، مع {FIXED_REMINDER}"',
        
        "الفضية": f'{emoji} **نسبة الحل {percentage:.1f}% (الفضية)**\n\n"متوسط الإنجاز في المادة يعكس تفاعلًا مقبولًا (فئة فضية). يُوصى بتعزيز المتابعة و{PARENT_COMMUNICATION}، مع {FIXED_REMINDER}"',
        
        "البرونزية": f'{emoji} **نسبة الحل {percentage:.1f}% (البرونزية)**\n\n"نسبة الإنجاز متوسطة (فئة برونزية). يُوصى بزيادة المتابعة و{PARENT_COMMUNICATION} لتحفيز الطلاب، مع {FIXED_REMINDER}"',
        
        "يحتاج إلى تحسين": f'{emoji} **نسبة الحل {percentage:.1f}% (يحتاج إلى تحسين)**\n\n"المادة أظهرت ضعفًا في إنجاز التقييمات. يُوصى بتدخل مباشر مع تفعيل {PARENT_COMMUNICATION}، مع {FIXED_REMINDER}"',
        
        "غير مستفيد": f'{emoji} **نسبة الحل {percentage:.1f}% (غير مستفيد)**\n\n"لم يتم تسجيل أي إنجاز في التقييمات الأسبوعية. يُوصى بمتابعة عاجلة مع تكثيف {PARENT_COMMUNICATION}، مع {FIXED_REMINDER}"'
    }
    
    return recommendations.get(band, f"نسبة الحل: {percentage:.1f}%")


def get_student_recommendation_by_percentage(percentage, student_name):
    """
    Generate recommendation for individual student based on completion percentage.
    
    Args:
        percentage: Student's completion percentage
        student_name: Name of the student
    
    Returns:
        str: Arabic recommendation text
    """
    if percentage is None:
        return f"لا توجد بيانات كافية لتقييم أداء الطالب {student_name}."
    
    band = get_band_from_percentage(percentage)
    emoji = get_band_emoji(band)
    
    recommendations = {
        "البلاتينية": f'{emoji} **أداء بلاتيني ({percentage:.1f}%)**\n\nالطالب ملتزم بشكل ممتاز. نوصي بالاستمرار والتشجيع.',
        
        "الذهبية": f'{emoji} **أداء ذهبي ({percentage:.1f}%)**\n\nالطالب يحقق أداءً ذهبيًا. نوصي بمزيد من التحفيز للوصول للبلاتينية.',
        
        "الفضية": f'{emoji} **أداء فضي ({percentage:.1f}%)**\n\nالطالب يحتاج إلى مزيد من الالتزام. نوصي بالمتابعة المستمرة.',
        
        "البرونزية": f'{emoji} **أداء برونزي ({percentage:.1f}%)**\n\nالطالب يحتاج إلى متابعة مكثفة. نوصي بالتذكير المستمر والتحفيز.',
        
        "يحتاج إلى تحسين": f'{emoji} **يحتاج إلى تحسين ({percentage:.1f}%)**\n\nالطالب يحتاج إلى تدخل عاجل. نوصي بـ {PARENT_COMMUNICATION} ووضع خطة متابعة يومية.',
        
        "غير مستفيد": f'{emoji} **غير مستفيد ({percentage:.1f}%)**\n\nالطالب لم ينجز أي تقييم. نوصي بـ {PARENT_COMMUNICATION} العاجل واجتماع فوري مع ولي الأمر.'
    }
    
    return recommendations.get(band, f"نسبة الإنجاز: {percentage:.1f}%")


# Legacy functions for backward compatibility
def get_recommendation_for_band(band, student_name=None, level='student'):
    """Legacy function - maps old bands to new system."""
    # Map old bands to percentages
    band_to_percentage = {
        "Platinum": 97.5,
        "Gold": 89.5,
        "Silver": 77.5,
        "Bronze": 60,
        "Needs Improvement": 30,
        "N/A": None
    }
    
    percentage = band_to_percentage.get(band)
    
     # If band is already in Arabic, get percentage from band name
    if band in BAND_LABELS:
        # Get percentage from band name (new system)
        if band == "البلاتينية":
            percentage = 95.0
        elif band == "الذهبية":
            percentage = 82.0
        elif band == "الفضية":
            percentage = 67.0
        elif band == "البرونزية":
            percentage = 50.0
        elif band == "يحتاج إلى تحسين":
            percentage = 20.0
        elif band == "غير مستفيد":
            percentage = 0.0
        else:
            percentage = None
    
    if level == 'class':
        return get_class_recommendation_by_percentage(percentage, student_name or "الصف")
    else:
        return get_student_recommendation_by_percentage(percentage, student_name or "الطالب")


def get_class_recommendations(class_stats, sheet_name):
    """
    Generate recommendations for an entire class based on statistics.
    
    Args:
        class_stats: Class statistics dictionary
        sheet_name: Name of the subject/class
    
    Returns:
        str: Arabic recommendation text for the class
    """
    avg_completion = class_stats.get('average_completion')
    return get_class_recommendation_by_percentage(avg_completion, sheet_name)


def generate_student_profile_recommendations(student_stats):
    """
    Generate recommendations for individual student profile.
    
    Args:
        student_stats: Student statistics dictionary
    
    Returns:
        str: Arabic recommendation text
    """
    overall_rate = student_stats.get('overall_completion_rate')
    student_name = "الطالب"
    
    return get_student_recommendation_by_percentage(overall_rate, student_name)

