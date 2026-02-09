#!/usr/bin/env python3
"""
=================================================================
نظام أتمتة شهادات الشكر والتقدير - التصميم الإبداعي
مدرسة عثمان بن عفان النموذجية للبنين
العام الأكاديمي 2025-2026
=================================================================
"""

import os
import json
import pandas as pd
from datetime import datetime
from generate_creative_cert import generate_creative_certificate

# ============================================================
# الإعدادات
# ============================================================
EXCEL_FILE = '/home/ubuntu/upload/متابعةضبطالأداء-.xlsx'
CERTIFICATES_DIR = '/home/ubuntu/enjaz_automation/certificates_creative'
SCORE_COLUMN = 'جودة الأداء على قطر للتعليم-الدرجة النهائية 8'
TARGET_SCORE = 8.0
SENT_COLUMN = 'sent'
SENT_VALUE = 'تم الارسال'


def read_excel_data(excel_path):
    """قراءة ملف الإكسل واستخراج المعلمين الحاصلين على 8"""
    all_teachers = []
    
    # قراءة ورقة المعلمات
    df1 = pd.read_excel(excel_path, sheet_name='المعلمات')
    teachers_8_sheet1 = df1[df1[SCORE_COLUMN] == TARGET_SCORE].copy()
    
    for _, row in teachers_8_sheet1.iterrows():
        teacher = {
            'name': str(row['اسم المعلم']).strip(),
            'subject': str(row.get('المادة', '')).strip(),
            'email': str(row.get('Teacheremail', '')).strip(),
            'score': row[SCORE_COLUMN],
            'sent': str(row.get(SENT_COLUMN, '')).strip(),
            'sheet': 'المعلمات'
        }
        all_teachers.append(teacher)
    
    # قراءة ورقة الطفولة
    df2 = pd.read_excel(excel_path, sheet_name='الطفولة')
    if SCORE_COLUMN in df2.columns:
        teachers_8_sheet2 = df2[df2[SCORE_COLUMN] == TARGET_SCORE].copy()
        
        for _, row in teachers_8_sheet2.iterrows():
            teacher = {
                'name': str(row['اسم المعلم']).strip(),
                'subject': str(row.get('المادة', '')).strip(),
                'email': str(row.get('Teacheremail', '')).strip(),
                'score': row[SCORE_COLUMN],
                'sent': str(row.get(SENT_COLUMN, '')).strip(),
                'sheet': 'الطفولة'
            }
            all_teachers.append(teacher)
    
    return all_teachers


def generate_all_certificates(teachers):
    """توليد شهادات إبداعية لجميع المعلمين"""
    os.makedirs(CERTIFICATES_DIR, exist_ok=True)
    
    generated = []
    for i, teacher in enumerate(teachers, 1):
        name = teacher['name']
        subject = teacher['subject']
        safe_name = name.replace(' ', '_').replace('/', '_')
        output_path = os.path.join(CERTIFICATES_DIR, f"شهادة_{safe_name}.png")
        
        print(f"  [{i}/{len(teachers)}] ✅ {name} ({subject})")
        try:
            generate_creative_certificate(name, subject, output_path)
            teacher['certificate_path'] = output_path
            generated.append(teacher)
        except Exception as e:
            print(f"  ❌ خطأ: {name}: {e}")
    
    return generated


def prepare_teams_post(teachers):
    """تجهيز نص بوست اليمز"""
    names_list = '\n'.join([f"⭐ {t['name']} - {t['subject']}" for t in teachers])
    
    post_text = f"""🏆 شهادات شكر وتقدير 🏆

يسر إدارة مدرسة عثمان بن عفان النموذجية للبنين أن تتقدم بخالص الشكر والتقدير للمعلمات المتميزات الحاصلات على الدرجة الكاملة (8/8) في جودة الأداء على نظام قطر للتعليم:

{names_list}

تهانينا لجميع المعلمات المتميزات! 🎉
مع تمنياتنا بدوام التوفيق والتميز

#التعليم_الإلكتروني #قطر_للتعليم #تميز #مدرسة_عثمان_بن_عفان"""
    
    return post_text


def main():
    print("=" * 60)
    print("🚀 نظام أتمتة شهادات الشكر والتقدير - التصميم الإبداعي")
    print("=" * 60)
    
    # الخطوة 1: قراءة ملف الإكسل
    print("\n📊 الخطوة 1: قراءة ملف الإكسل...")
    teachers = read_excel_data(EXCEL_FILE)
    print(f"   المعلمين الحاصلين على الدرجة الكاملة (8): {len(teachers)}")
    
    # الخطوة 2: توليد الشهادات
    print(f"\n📜 الخطوة 2: توليد الشهادات الإبداعية ({len(teachers)} شهادة)...")
    generated = generate_all_certificates(teachers)
    print(f"\n   ✅ تم توليد {len(generated)} شهادة بنجاح")
    
    # الخطوة 3: تجهيز بوست اليمز
    print("\n📱 الخطوة 3: تجهيز بوست اليمز...")
    post_text = prepare_teams_post(generated)
    post_path = os.path.join(CERTIFICATES_DIR, 'teams_post.txt')
    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(post_text)
    print(f"   تم حفظ نص البوست في: {post_path}")
    
    # حفظ الملخص
    summary = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'total_certificates': len(generated),
        'teachers': [
            {
                'name': t['name'],
                'subject': t['subject'],
                'email': t['email'],
                'certificate': t.get('certificate_path', ''),
                'sheet': t['sheet']
            }
            for t in generated
        ]
    }
    
    summary_path = os.path.join(CERTIFICATES_DIR, 'summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"✅ تم الانتهاء! {len(generated)} شهادة في: {CERTIFICATES_DIR}")
    print("=" * 60)
    
    return generated


if __name__ == '__main__':
    main()
