"""
Parent Recommendations Module for Enjaz Application.
Generates Arabic recommendations for parents based on student performance bands.
"""

from enjaz.analysis import get_band


def get_parent_recommendation(completion_rate):
    """
    Generate recommendation for parents based on student's completion rate.
    
    Args:
        completion_rate: Student's completion percentage (0-100)
    
    Returns:
        str: Arabic recommendation text for parents
    """
    band = get_band(completion_rate)
    
    recommendations = {
        "البلاتينية": (
            "🏆 **الفئة البلاتينية (90% – 100%)**\n\n"
            "تُظهر النتائج التزامًا مرتفعًا جدًا بحل التقييمات الأسبوعية على نظام قطر للتعليم (فئة بلاتينية). "
            "نشكر تعاونكم، ويُوصى بالاستمرار في الدعم والتحفيز للحفاظ على هذا المستوى المتميز."
        ),
        
        "الذهبية": (
            "🥇 **الفئة الذهبية (75% – أقل من 90%)**\n\n"
            "تُظهر النتائج التزامًا جيدًا جدًا وقريبًا من مستوى الامتياز (فئة ذهبية). "
            "دعمكم المستمر يُعزّز الوصول إلى التميز الكامل."
        ),
        
        "الفضية": (
            "🥈 **الفئة الفضية (60% – أقل من 75%)**\n\n"
            "النسبة الحالية جيدة وتعكس تقدّمًا ملحوظًا (فئة فضية). "
            "يُوصى بمتابعة دورية وتشجيع مستمر لرفع مستوى الالتزام."
        ),
        
        "البرونزية": (
            "🥉 **الفئة البرونزية (40% – أقل من 60%)**\n\n"
            "النسبة متوسطة منخفضة (فئة برونزية). "
            "يُوصى بتكثيف التشجيع والتواصل الدوري لرفع مستوى الالتزام بحل التقييمات."
        ),
        
        "يحتاج إلى تطوير": (
            "🔧 **يحتاج إلى تطوير (أقل من 40%)**\n\n"
            "النسبة الحالية منخفضة وتحتاج إلى رفع ملحوظ. "
            "يُوصى بزيادة المتابعة والتواصل المستمر لتكوين عادات منتظمة في إنجاز التقييمات."
        ),
        
        "لا يستفيد من النظام": (
            "🚫 **لا يستفيد من النظام / لم ينجز (0%)**\n\n"
            "لا توجد إنجازات مسجلة في التقييمات الأسبوعية حتى الآن. "
            "يُوصى بتواصل عاجل وتحفيز مباشر للبدء فورًا في حل التقييمات على نظام قطر للتعليم."
        )
    }
    
    return recommendations.get(band, "لا توجد توصيات متاحة.")


def format_parent_communication_email(student_name, completion_rate, subjects_summary):
    """
    Format a complete email for parent communication.
    
    Args:
        student_name: Name of the student
        completion_rate: Overall completion percentage
        subjects_summary: List of dicts with subject details
    
    Returns:
        str: Formatted email text in Arabic
    """
    band = get_band(completion_rate)
    recommendation = get_parent_recommendation(completion_rate)
    
    email = f"""
السلام عليكم ورحمة الله وبركاته

ولي أمر الطالب/ة: {student_name}

نود إطلاعكم على أداء الطالب/ة في التقييمات الأسبوعية على نظام قطر للتعليم:

**نسبة الإنجاز الإجمالية:** {completion_rate:.1f}%
**الفئة:** {band}

---

**تفاصيل الأداء حسب المواد:**

"""
    
    for subject in subjects_summary:
        email += f"• {subject['name']}: {subject['completed']}/{subject['total']} ({subject['rate']:.1f}%)\n"
    
    email += f"""

---

**التوصيات:**

{recommendation}

---

نشكر تعاونكم المستمر ونتطلع لدعمكم في تحفيز الطالب/ة على الالتزام بحل التقييمات الأسبوعية.

مع خالص التحية،
إدارة مدرسة عثمان بن عفان النموذجية
"""
    
    return email

