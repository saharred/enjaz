#!/usr/bin/env python3
"""
=================================================================
🚀 نظام أتمتة شهادات الشكر والتقدير
مدرسة عثمان بن عفان النموذجية للبنين
العام الأكاديمي 2025-2026
=================================================================

الخطوات:
1. قراءة ملف الإكسل واستخراج المعلمين الحاصلين على الدرجة الكاملة (8)
2. توليد شهادة إبداعية لكل معلم/معلمة
3. إرسال الشهادات عبر Gmail لمجموعة المدرسة
4. تجهيز بوست اليمز (Teams/Yammer)

=================================================================
"""

import os
import sys
import json
import subprocess
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# =============================================================
# ⚙️ المتغيرات - عدّليها حسب احتياجك
# =============================================================

# مسار ملف الإكسل
EXCEL_FILE = '/home/ubuntu/upload/متابعةضبطالأداء-.xlsx'

# أسماء أوراق العمل في الإكسل
SHEET_NAMES = ['المعلمات', 'الطفولة']

# اسم عمود الدرجة
SCORE_COLUMN = 'جودة الأداء على قطر للتعليم-الدرجة النهائية 8'

# الدرجة المطلوبة
TARGET_SCORE = 8.0

# اسم عمود حالة الإرسال
SENT_COLUMN = 'sent'

# قيمة "تم الإرسال"
SENT_VALUE = 'تم الارسال'

# هل نرسل فقط للي ما تم إرسال لهم؟ (True = فقط الجدد، False = الكل)
ONLY_NEW = False

# إيميل مجموعة المدرسة (غيّريه لإيميل مجموعتك)
GROUP_EMAIL = 'school-group@education.qa'

# موضوع الإيميل
EMAIL_SUBJECT = 'شهادة شكر وتقدير - الدرجة الكاملة في جودة الأداء'

# نص الشهادة - السبب
CERT_REASON_LINE1 = 'وذلك تقديراً لتحقيقها شروط المحتوى الرقمي'
CERT_REASON_LINE2 = 'على نظام قطر للتعليم خلال شهر يناير'
CERT_REASON_LINE3 = 'مع تمنياتنا لها بالتوفيق والتميز'

# نص الإيميل
EMAIL_BODY = """السلام عليكم ورحمة الله وبركاته

تتقدم إدارة مدرسة عثمان بن عفان النموذجية للبنين بخالص الشكر والتقدير
للمعلمات المتميزات لتحقيقهن شروط المحتوى الرقمي على نظام قطر للتعليم خلال شهر يناير.

مرفق شهادات الشكر والتقدير.

مع تمنياتنا بدوام التوفيق والتميز.

منسقة المشاريع الإلكترونية
سحر عثمان"""

# مجلد حفظ الشهادات
CERTIFICATES_DIR = '/home/ubuntu/enjaz_automation/certificates_final'

# مسار خلفية الشهادة
BG_PATH = '/home/ubuntu/enjaz_automation/templates/certificate_bg_new.png'

# مسار شعار الوزارة
LOGO_PATH = '/home/ubuntu/enjaz_automation/templates/ministry_logo2.png'

# معلومات الترويسة
SCHOOL_NAME = 'مدرسة عثمان بن عفان النموذجية للبنين'
ACADEMIC_YEAR = '2025 - 2026'
DEPARTMENT = 'التعليم الإلكتروني'

# معلومات التوقيعات
SIGNATURES = {
    'right': {'title': 'منسقة المشاريع الإلكترونية', 'name': 'سحر عثمان'},
    'center': {'title': 'النائب الأكاديمي', 'name': 'مريم القضع'},
    'left': {'title': 'مدير المدرسة', 'name': 'منيرة الهاجري'},
}

VISION = 'رؤيتنا: متعلم ريادي لتنمية مستدامة'


# =============================================================
# 🎨 إعدادات التصميم
# =============================================================

# مسارات الخطوط
FONT_BOLD = '/usr/share/fonts/truetype/noto/NotoKufiArabic-Bold.ttf'
FONT_NASKH_BOLD = '/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf'
FONT_KUFI_REGULAR = '/usr/share/fonts/truetype/noto/NotoKufiArabic-Regular.ttf'
FONT_AMIRI = '/usr/share/fonts/opentype/fonts-hosny-amiri/Amiri-Bold.ttf'
FONT_AMIRI_REG = '/usr/share/fonts/opentype/fonts-hosny-amiri/Amiri-Regular.ttf'

# الألوان
MAROON = (139, 26, 43)
GOLD = (201, 168, 76)
DARK_TEXT = (60, 40, 30)
LIGHT_TEXT = (100, 80, 60)
WHITE = (255, 255, 255)
CREAM_ALPHA = (250, 245, 235, 200)


# =============================================================
# 🔧 دوال مساعدة
# =============================================================

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def get_text_bbox(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def draw_centered_text(draw, text, y, font, fill, img_width):
    w, h = get_text_bbox(draw, text, font)
    x = (img_width - w) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return h


# =============================================================
# 📊 الخطوة 1: قراءة ملف الإكسل
# =============================================================

def read_excel_data():
    """قراءة ملف الإكسل واستخراج المعلمين الحاصلين على الدرجة المطلوبة"""
    all_teachers = []
    
    for sheet_name in SHEET_NAMES:
        try:
            df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)
            if SCORE_COLUMN not in df.columns:
                print(f"  ⚠️ عمود الدرجة غير موجود في ورقة: {sheet_name}")
                continue
            
            teachers_filtered = df[df[SCORE_COLUMN] == TARGET_SCORE].copy()
            
            for _, row in teachers_filtered.iterrows():
                sent_status = str(row.get(SENT_COLUMN, '')).strip()
                
                # تخطي اللي تم إرسال لهم إذا ONLY_NEW = True
                if ONLY_NEW and sent_status == SENT_VALUE:
                    continue
                
                teacher = {
                    'name': str(row['اسم المعلم']).strip(),
                    'subject': str(row.get('المادة', '')).strip(),
                    'email': str(row.get('Teacheremail', '')).strip(),
                    'score': row[SCORE_COLUMN],
                    'sent': sent_status,
                    'sheet': sheet_name
                }
                all_teachers.append(teacher)
            
            print(f"  ✅ ورقة '{sheet_name}': {len(teachers_filtered)} معلم/معلمة بدرجة {int(TARGET_SCORE)}")
        except Exception as e:
            print(f"  ❌ خطأ في قراءة ورقة '{sheet_name}': {e}")
    
    return all_teachers


# =============================================================
# 📜 الخطوة 2: توليد الشهادات
# =============================================================

def generate_certificate(teacher_name, subject, output_path):
    """توليد شهادة إبداعية لمعلم واحد"""
    
    bg = Image.open(BG_PATH).convert('RGBA')
    img_w, img_h = bg.size
    
    overlay = Image.new('RGBA', (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # شريط شبه شفاف للهيدر
    header_strip = Image.new('RGBA', (img_w, 90), CREAM_ALPHA)
    overlay.paste(header_strip, (0, 50))
    
    # شريط شبه شفاف للفوتر
    footer_strip = Image.new('RGBA', (img_w - 160, 130), CREAM_ALPHA)
    overlay.paste(footer_strip, (80, img_h - 240))
    
    draw = ImageDraw.Draw(overlay)
    
    # الشعار
    logo = Image.open(LOGO_PATH).convert('RGBA')
    logo_size = 100
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    logo_x = (img_w - logo_size) // 2
    logo_y = 55
    
    # الخطوط
    font_ministry = get_font(FONT_BOLD, 22)
    font_ministry_en = get_font(FONT_KUFI_REGULAR, 18)
    font_school = get_font(FONT_BOLD, 32)
    font_year = get_font(FONT_KUFI_REGULAR, 22)
    font_elearn = get_font(FONT_BOLD, 24)
    font_title = get_font(FONT_AMIRI, 64)
    font_intro = get_font(FONT_NASKH_BOLD, 28)
    font_name = get_font(FONT_AMIRI, 58)
    font_subject = get_font(FONT_BOLD, 26)
    font_reason = get_font(FONT_AMIRI_REG, 24)
    font_footer_title = get_font(FONT_BOLD, 22)
    font_footer_name = get_font(FONT_NASKH_BOLD, 22)
    font_vision = get_font(FONT_KUFI_REGULAR, 18)
    font_stars = get_font(FONT_AMIRI, 30)
    
    # --- الهيدر ---
    draw.text((img_w - 160, 65), "دولة قطر", font=font_ministry, fill=WHITE, anchor='rt')
    draw.text((img_w - 160, 95), "وزارة التربية والتعليم والتعليم العالي", font=font_ministry, fill=WHITE, anchor='rt')
    draw.text((160, 65), "State of Qatar", font=font_ministry_en, fill=WHITE, anchor='lt')
    draw.text((160, 92), "Ministry of Education & Higher Education", font=font_ministry_en, fill=WHITE, anchor='lt')
    
    # --- معلومات المدرسة ---
    y = 175
    h = draw_centered_text(draw, SCHOOL_NAME, y, font_school, MAROON, img_w)
    y += h + 10
    h = draw_centered_text(draw, f"العام الأكاديمي {ACADEMIC_YEAR}", y, font_year, LIGHT_TEXT, img_w)
    y += h + 6
    h = draw_centered_text(draw, DEPARTMENT, y, font_elearn, MAROON, img_w)
    
    # خط ذهبي
    y += h + 12
    line_w = 450
    line_x = (img_w - line_w) // 2
    draw.line([(line_x, y), (line_x + line_w, y)], fill=GOLD, width=3)
    
    # --- عنوان الشهادة ---
    y += 18
    h = draw_centered_text(draw, "شهادة شكر وتقدير", y, font_title, MAROON, img_w)
    y += h + 3
    h = draw_centered_text(draw, "✦     ✦     ✦", y, font_stars, GOLD, img_w)
    
    # المقدمة
    y += h + 12
    h = draw_centered_text(draw, "تتقدم إدارة المدرسة بخالص الشكر والتقدير إلى", y, font_intro, DARK_TEXT, img_w)
    
    # --- اسم المعلم ---
    y += h + 22
    name_w, name_h = get_text_bbox(draw, teacher_name, font_name)
    name_x = (img_w - name_w) // 2
    draw.text((name_x, y), teacher_name, font=font_name, fill=MAROON)
    
    y_line = y + name_h + 4
    draw.line([(name_x - 20, y_line), (name_x + name_w + 20, y_line)], fill=GOLD, width=4)
    
    # المادة
    y = y_line + 12
    h = draw_centered_text(draw, f"معلمة مادة: {subject}", y, font_subject, GOLD, img_w)
    
    # --- السبب ---
    y += h + 18
    h = draw_centered_text(draw, CERT_REASON_LINE1, y, font_reason, DARK_TEXT, img_w)
    y += h + 5
    h = draw_centered_text(draw, CERT_REASON_LINE2, y, font_reason, DARK_TEXT, img_w)
    y += h + 5
    h = draw_centered_text(draw, CERT_REASON_LINE3, y, font_reason, DARK_TEXT, img_w)
    y += h + 8
    draw_centered_text(draw, "★     ★     ★", y, font_stars, GOLD, img_w)
    
    # --- الفوتر ---
    footer_y = img_h - 225
    
    col_right_x = img_w - 380
    draw.text((col_right_x, footer_y), SIGNATURES['right']['title'], font=font_footer_title, fill=MAROON, anchor='mt')
    draw.line([(col_right_x - 100, footer_y + 35), (col_right_x + 100, footer_y + 35)], fill=MAROON, width=2)
    draw.text((col_right_x, footer_y + 45), SIGNATURES['right']['name'], font=font_footer_name, fill=DARK_TEXT, anchor='mt')
    
    col_center_x = img_w // 2
    draw.text((col_center_x, footer_y), SIGNATURES['center']['title'], font=font_footer_title, fill=MAROON, anchor='mt')
    draw.line([(col_center_x - 100, footer_y + 35), (col_center_x + 100, footer_y + 35)], fill=MAROON, width=2)
    draw.text((col_center_x, footer_y + 45), SIGNATURES['center']['name'], font=font_footer_name, fill=DARK_TEXT, anchor='mt')
    
    col_left_x = 380
    draw.text((col_left_x, footer_y), SIGNATURES['left']['title'], font=font_footer_title, fill=MAROON, anchor='mt')
    draw.line([(col_left_x - 100, footer_y + 35), (col_left_x + 100, footer_y + 35)], fill=MAROON, width=2)
    draw.text((col_left_x, footer_y + 45), SIGNATURES['left']['name'], font=font_footer_name, fill=DARK_TEXT, anchor='mt')
    
    # الرؤية
    vision_y = img_h - 135
    draw_centered_text(draw, VISION, vision_y, font_vision, MAROON, img_w)
    
    # --- التركيب النهائي ---
    result = Image.alpha_composite(bg, overlay)
    result.paste(logo, (logo_x, logo_y), logo)
    result_rgb = result.convert('RGB')
    result_rgb.save(output_path, 'PNG', quality=95)
    return output_path


def generate_all_certificates(teachers):
    """توليد شهادات لجميع المعلمين"""
    os.makedirs(CERTIFICATES_DIR, exist_ok=True)
    
    generated = []
    for i, teacher in enumerate(teachers, 1):
        name = teacher['name']
        subject = teacher['subject']
        safe_name = name.replace(' ', '_').replace('/', '_')
        output_path = os.path.join(CERTIFICATES_DIR, f"شهادة_{safe_name}.png")
        
        print(f"  [{i}/{len(teachers)}] ✅ {name} ({subject})")
        try:
            generate_certificate(name, subject, output_path)
            teacher['certificate_path'] = output_path
            generated.append(teacher)
        except Exception as e:
            print(f"  ❌ خطأ في {name}: {e}")
    
    return generated


# =============================================================
# 📧 الخطوة 3: إرسال الشهادات عبر Gmail
# =============================================================

def send_certificates_via_gmail(teachers):
    """إرسال الشهادات عبر Gmail MCP"""
    
    # تجميع مسارات الشهادات
    attachments = [t['certificate_path'] for t in teachers if 'certificate_path' in t]
    
    if not attachments:
        print("  ❌ لا توجد شهادات للإرسال")
        return False
    
    # بناء أمر MCP
    message_data = {
        "messages": [{
            "subject": EMAIL_SUBJECT,
            "to": [GROUP_EMAIL],
            "content": EMAIL_BODY,
            "attachments": attachments
        }]
    }
    
    cmd = [
        'manus-mcp-cli', 'tool', 'call', 'gmail_send_messages',
        '--server', 'gmail',
        '--input', json.dumps(message_data, ensure_ascii=False)
    ]
    
    print(f"  📧 إرسال {len(attachments)} شهادة إلى: {GROUP_EMAIL}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"  ✅ تم الإرسال بنجاح!")
            return True
        else:
            print(f"  ❌ خطأ: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ خطأ في الإرسال: {e}")
        return False


# =============================================================
# 📱 الخطوة 4: تجهيز بوست اليمز
# =============================================================

def prepare_teams_post(teachers):
    """تجهيز نص بوست اليمز/Teams"""
    names_list = '\n'.join([f"⭐ {t['name']} - {t['subject']}" for t in teachers])
    
    post_text = f"""🏆 شهادات شكر وتقدير 🏆

يسر إدارة {SCHOOL_NAME} أن تتقدم بخالص الشكر والتقدير للمعلمات المتميزات الحاصلات على الدرجة الكاملة (8/8) في جودة الأداء على نظام قطر للتعليم:

{names_list}

تهانينا لجميع المعلمات المتميزات! 🎉
مع تمنياتنا بدوام التوفيق والتميز

{DEPARTMENT} - {SCHOOL_NAME}
العام الأكاديمي {ACADEMIC_YEAR}

#التعليم_الإلكتروني #قطر_للتعليم #تميز #مدرسة_عثمان_بن_عفان"""
    
    return post_text


# =============================================================
# 🚀 التشغيل الرئيسي
# =============================================================

def main():
    print("=" * 65)
    print("🚀 نظام أتمتة شهادات الشكر والتقدير")
    print(f"   {SCHOOL_NAME}")
    print(f"   العام الأكاديمي {ACADEMIC_YEAR}")
    print("=" * 65)
    
    # --- الخطوة 1: قراءة الإكسل ---
    print("\n📊 الخطوة 1: قراءة ملف الإكسل...")
    teachers = read_excel_data()
    print(f"   إجمالي المعلمين المؤهلين: {len(teachers)}")
    
    if not teachers:
        print("❌ لا يوجد معلمين بالدرجة المطلوبة!")
        return
    
    # --- الخطوة 2: توليد الشهادات ---
    print(f"\n📜 الخطوة 2: توليد {len(teachers)} شهادة...")
    generated = generate_all_certificates(teachers)
    print(f"\n   ✅ تم توليد {len(generated)} شهادة")
    
    # --- الخطوة 3: إرسال Gmail ---
    print(f"\n📧 الخطوة 3: إرسال الشهادات عبر Gmail...")
    print(f"   المرسل إليه: {GROUP_EMAIL}")
    send_certificates_via_gmail(generated)
    
    # --- الخطوة 4: بوست اليمز ---
    print(f"\n📱 الخطوة 4: تجهيز بوست اليمز...")
    post_text = prepare_teams_post(generated)
    post_path = os.path.join(CERTIFICATES_DIR, 'teams_post.txt')
    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(post_text)
    print(f"   ✅ تم حفظ نص البوست في: {post_path}")
    
    # --- حفظ الملخص ---
    summary = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'total': len(generated),
        'group_email': GROUP_EMAIL,
        'teachers': [
            {'name': t['name'], 'subject': t['subject'], 'email': t['email'], 'sheet': t['sheet']}
            for t in generated
        ]
    }
    summary_path = os.path.join(CERTIFICATES_DIR, 'summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 65)
    print(f"✅ تم الانتهاء بنجاح!")
    print(f"   📜 {len(generated)} شهادة في: {CERTIFICATES_DIR}")
    print(f"   📧 تم الإرسال إلى: {GROUP_EMAIL}")
    print(f"   📱 بوست اليمز: {post_path}")
    print("=" * 65)


if __name__ == '__main__':
    main()
