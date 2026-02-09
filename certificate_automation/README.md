# نظام أتمتة شهادات الشكر والتقدير

## مدرسة عثمان بن عفان النموذجية للبنين | العام الأكاديمي 2025-2026

---

## الوصف

نظام أتمتة كامل لإنشاء وإرسال شهادات شكر وتقدير للمعلمين الحاصلين على الدرجة الكاملة (8/8) في جودة الأداء على نظام قطر للتعليم.

## خطوات الأتمتة

| الخطوة | الوصف |
|--------|-------|
| 1 | قراءة ملف الإكسل واستخراج المعلمين الحاصلين على الدرجة الكاملة |
| 2 | توليد شهادة إبداعية لكل معلم/معلمة باسمه ومادته |
| 3 | إرسال الشهادات عبر Gmail لمجموعة المدرسة |
| 4 | تجهيز بوست اليمز (Teams/Yammer) |

## الملفات

```
enjaz_automation/
├── main_automation.py          # الكود الرئيسي للأتمتة (مع المتغيرات)
├── generate_creative_cert.py   # مولّد الشهادات الإبداعية
├── automation_creative.py      # نسخة بديلة من الأتمتة
├── templates/
│   ├── certificate_bg_new.png  # خلفية الشهادة
│   └── ministry_logo2.png      # شعار الوزارة
├── certificates_final/         # الشهادات المولّدة
└── README.md                   # هذا الملف
```

## المتغيرات القابلة للتعديل

افتحي ملف `main_automation.py` وعدّلي المتغيرات التالية:

```python
# مسار ملف الإكسل
EXCEL_FILE = '/path/to/your/excel.xlsx'

# إيميل مجموعة المدرسة
GROUP_EMAIL = 'school-group@education.qa'

# هل نرسل فقط للجدد؟
ONLY_NEW = False  # True = فقط اللي ما تم إرسال لهم

# الدرجة المطلوبة
TARGET_SCORE = 8.0

# معلومات المدرسة
SCHOOL_NAME = 'مدرسة عثمان بن عفان النموذجية للبنين'
ACADEMIC_YEAR = '2025 - 2026'
```

## التشغيل

```bash
python3 main_automation.py
```

## المتطلبات

```
pip3 install pandas openpyxl pillow
```

## الخطوط المطلوبة

```bash
sudo apt install fonts-noto-core fonts-hosny-amiri
```
