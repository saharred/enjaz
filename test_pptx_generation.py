"""
Test script for PowerPoint generation.
"""

import sys
sys.path.insert(0, '/home/ubuntu/enjaz')

from enjaz.pptx_generator import generate_school_presentation

# Sample school statistics
school_stats = {
    'total_students': 150,
    'total_assessments': 450,
    'total_completed': 360,
    'completion_rate': 80.0,
    'band_distribution': {
        'البلاتينية': 25,
        'الذهبية': 40,
        'الفضية': 35,
        'البرونزية': 30,
        'يحتاج إلى تطوير من النظام': 15,
        'لا يستفيد من النظام': 5
    }
}

# Sample coordinator actions
coordinator_actions = """**الإجراءات المتخذة على مستوى المدرسة:**

**1. على المستوى الإداري:**
- عقد اجتماع طارئ مع جميع رؤساء الأقسام لمناقشة نتائج التقرير
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
"""

# Generate presentation
try:
    output_path = "/home/ubuntu/enjaz/test_school_presentation.pptx"
    result = generate_school_presentation(
        school_stats,
        coordinator_actions,
        output_path
    )
    print(f"✅ تم إنشاء العرض التقديمي بنجاح: {result}")
    
    # Check file size
    import os
    file_size = os.path.getsize(result)
    print(f"📊 حجم الملف: {file_size / 1024:.2f} KB")
    
except Exception as e:
    print(f"❌ حدث خطأ: {str(e)}")
    import traceback
    traceback.print_exc()

