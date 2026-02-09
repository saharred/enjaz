#!/usr/bin/env python3
"""
نظام توليد شهادات إبداعية بتصميم AI
مدرسة عثمان بن عفان النموذجية للبنين
"""

import os
from PIL import Image, ImageDraw, ImageFont


# Paths
BG_PATH = '/home/ubuntu/enjaz_automation/templates/certificate_bg.png'
LOGO_PATH = '/home/ubuntu/enjaz_automation/templates/ministry_logo2.png'
CERTIFICATES_DIR = '/home/ubuntu/enjaz_automation/certificates_creative'
os.makedirs(CERTIFICATES_DIR, exist_ok=True)

# Font paths
FONT_BOLD = '/usr/share/fonts/truetype/noto/NotoKufiArabic-Bold.ttf'
FONT_REGULAR = '/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf'
FONT_NASKH_BOLD = '/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf'
FONT_KUFI_REGULAR = '/usr/share/fonts/truetype/noto/NotoKufiArabic-Regular.ttf'
FONT_AMIRI = '/usr/share/fonts/opentype/fonts-hosny-amiri/Amiri-Bold.ttf'
FONT_AMIRI_REG = '/usr/share/fonts/opentype/fonts-hosny-amiri/Amiri-Regular.ttf'

# Colors
MAROON = (139, 26, 43)
GOLD = (201, 168, 76)
DARK_TEXT = (60, 40, 30)
LIGHT_TEXT = (100, 80, 60)
WHITE = (255, 255, 255)
CREAM_ALPHA = (250, 245, 235, 200)


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


def generate_creative_certificate(teacher_name, subject, output_path):
    """Generate a creative certificate with AI background"""
    
    # Load background
    bg = Image.open(BG_PATH).convert('RGBA')
    img_w, img_h = bg.size
    
    # Create overlay for text
    overlay = Image.new('RGBA', (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Add semi-transparent cream strip behind header for readability
    header_strip = Image.new('RGBA', (img_w, 90), CREAM_ALPHA)
    overlay.paste(header_strip, (0, 50))
    
    # Add semi-transparent cream strip behind footer for readability
    footer_strip = Image.new('RGBA', (img_w - 160, 130), CREAM_ALPHA)
    overlay.paste(footer_strip, (80, img_h - 240))
    
    draw = ImageDraw.Draw(overlay)
    
    # Load logo
    logo = Image.open(LOGO_PATH).convert('RGBA')
    logo_size = 100
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    logo_x = (img_w - logo_size) // 2
    logo_y = 55
    
    # Fonts
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
    
    # --- Header ---
    # Ministry Arabic - right
    draw.text((img_w - 160, 65), "دولة قطر", font=font_ministry, fill=WHITE, anchor='rt')
    draw.text((img_w - 160, 95), "وزارة التربية والتعليم والتعليم العالي", font=font_ministry, fill=WHITE, anchor='rt')
    
    # Ministry English - left
    draw.text((160, 65), "State of Qatar", font=font_ministry_en, fill=WHITE, anchor='lt')
    draw.text((160, 92), "Ministry of Education & Higher Education", font=font_ministry_en, fill=WHITE, anchor='lt')
    
    # --- School Info ---
    y = 175
    h = draw_centered_text(draw, "مدرسة عثمان بن عفان النموذجية للبنين", y, font_school, MAROON, img_w)
    y += h + 10
    h = draw_centered_text(draw, "العام الأكاديمي 2025 - 2026", y, font_year, LIGHT_TEXT, img_w)
    y += h + 6
    h = draw_centered_text(draw, "التعليم الإلكتروني", y, font_elearn, MAROON, img_w)
    
    # Gold line
    y += h + 12
    line_w = 450
    line_x = (img_w - line_w) // 2
    draw.line([(line_x, y), (line_x + line_w, y)], fill=GOLD, width=3)
    
    # --- Certificate Title ---
    y += 18
    h = draw_centered_text(draw, "شهادة شكر وتقدير", y, font_title, MAROON, img_w)
    
    # Stars
    y += h + 3
    h = draw_centered_text(draw, "✦     ✦     ✦", y, font_stars, GOLD, img_w)
    
    # Intro
    y += h + 12
    h = draw_centered_text(draw, "تتقدم إدارة المدرسة بخالص الشكر والتقدير إلى", y, font_intro, DARK_TEXT, img_w)
    
    # --- Teacher Name ---
    y += h + 22
    name_w, name_h = get_text_bbox(draw, teacher_name, font_name)
    name_x = (img_w - name_w) // 2
    draw.text((name_x, y), teacher_name, font=font_name, fill=MAROON)
    
    # Gold underline
    y_line = y + name_h + 4
    draw.line([(name_x - 20, y_line), (name_x + name_w + 20, y_line)], fill=GOLD, width=4)
    
    # Subject
    y = y_line + 12
    h = draw_centered_text(draw, f"معلمة مادة: {subject}", y, font_subject, GOLD, img_w)
    
    # --- Reason ---
    y += h + 18
    h = draw_centered_text(draw, "وذلك تقديراً لحصولها على الدرجة الكاملة (8/8) في جودة الأداء", y, font_reason, DARK_TEXT, img_w)
    y += h + 5
    h = draw_centered_text(draw, "على نظام قطر للتعليم", y, font_reason, DARK_TEXT, img_w)
    y += h + 5
    h = draw_centered_text(draw, "مع تمنياتنا بدوام التوفيق والتميز", y, font_reason, DARK_TEXT, img_w)
    
    # Stars
    y += h + 8
    draw_centered_text(draw, "★     ★     ★", y, font_stars, GOLD, img_w)
    
    # --- Footer ---
    footer_y = img_h - 225
    
    # Right - منسقة المشاريع
    col_right_x = img_w - 380
    draw.text((col_right_x, footer_y), "منسقة المشاريع الإلكترونية", font=font_footer_title, fill=MAROON, anchor='mt')
    draw.line([(col_right_x - 100, footer_y + 35), (col_right_x + 100, footer_y + 35)], fill=MAROON, width=2)
    draw.text((col_right_x, footer_y + 45), "سحر عثمان", font=font_footer_name, fill=DARK_TEXT, anchor='mt')
    
    # Center - النائب الأكاديمي
    col_center_x = img_w // 2
    draw.text((col_center_x, footer_y), "النائب الأكاديمي", font=font_footer_title, fill=MAROON, anchor='mt')
    draw.line([(col_center_x - 100, footer_y + 35), (col_center_x + 100, footer_y + 35)], fill=MAROON, width=2)
    draw.text((col_center_x, footer_y + 45), "مريم القضع", font=font_footer_name, fill=DARK_TEXT, anchor='mt')
    
    # Left - مدير المدرسة
    col_left_x = 380
    draw.text((col_left_x, footer_y), "مدير المدرسة", font=font_footer_title, fill=MAROON, anchor='mt')
    draw.line([(col_left_x - 100, footer_y + 35), (col_left_x + 100, footer_y + 35)], fill=MAROON, width=2)
    draw.text((col_left_x, footer_y + 45), "منيرة الهاجري", font=font_footer_name, fill=DARK_TEXT, anchor='mt')
    
    # Vision
    vision_y = img_h - 135
    draw_centered_text(draw, "رؤيتنا: متعلم ريادي لتنمية مستدامة", vision_y, font_vision, MAROON, img_w)
    
    # --- Composite ---
    result = Image.alpha_composite(bg, overlay)
    result.paste(logo, (logo_x, logo_y), logo)
    result_rgb = result.convert('RGB')
    result_rgb.save(output_path, 'PNG', quality=95)
    
    return output_path


if __name__ == '__main__':
    test_name = "دعاء سيد اسماعيل محمد"
    test_subject = "رياضيات"
    output = os.path.join(CERTIFICATES_DIR, f"شهادة_{test_name.replace(' ', '_')}.png")
    print(f"Generating: {test_name}")
    generate_creative_certificate(test_name, test_subject, output)
    print(f"Done: {output}")
    
    test_name2 = "نوف المري"
    test_subject2 = "الحوسبة و تكنولوجيا المعلومات"
    output2 = os.path.join(CERTIFICATES_DIR, f"شهادة_{test_name2.replace(' ', '_')}.png")
    print(f"Generating: {test_name2}")
    generate_creative_certificate(test_name2, test_subject2, output2)
    print(f"Done: {output2}")
