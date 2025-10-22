"""
Email Sender Module for Enjaz Application.
Sends teacher reports via email with attachments.
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional


def send_teacher_report_email(
    recipient_email: str,
    teacher_name: str,
    report_file_path: str,
    subject_count: int,
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 587,
    sender_email: Optional[str] = None,
    sender_password: Optional[str] = None
) -> tuple[bool, str]:
    """
    Send teacher report via email.
    
    Args:
        recipient_email: Teacher's email address
        teacher_name: Teacher's name
        report_file_path: Path to Excel report file
        subject_count: Number of subjects/classes in report
        smtp_server: SMTP server address
        smtp_port: SMTP port
        sender_email: Sender's email (from environment or config)
        sender_password: Sender's password (from environment or config)
    
    Returns:
        tuple: (success: bool, message: str)
    """
    
    # Get credentials from environment if not provided
    if not sender_email:
        sender_email = os.getenv('ENJAZ_SENDER_EMAIL', 'noreply@enjaz.qa')
    
    if not sender_password:
        sender_password = os.getenv('ENJAZ_SENDER_PASSWORD', '')
    
    # Validate inputs
    if not recipient_email or '@' not in recipient_email:
        return False, "❌ البريد الإلكتروني غير صحيح"
    
    if not os.path.exists(report_file_path):
        return False, "❌ ملف التقرير غير موجود"
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"تقرير إنجاز - {teacher_name}"
        
        # Email body in Arabic
        body = f"""
السلام عليكم ورحمة الله وبركاته،

الأستاذ/ة {teacher_name} المحترم/ة،

نرفق لكم تقريركم التحليلي من نظام إنجاز لتحليل التقييمات الإلكترونية الأسبوعية.

📊 **تفاصيل التقرير:**
- عدد المواد/الشعب: {subject_count}
- التقرير يتضمن: إحصائيات شاملة، توزيع الفئات، وأسماء الطلاب حسب الأداء

💡 **ملاحظات:**
- يرجى مراجعة التقرير واتخاذ الإجراءات اللازمة
- للاستفسارات، يرجى التواصل مع الإدارة

---

**رؤيتنا:** "متعلم ريادي لتنمية مستدامة" 🎯

© 2025 — مدرسة عثمان بن عفّان النموذجية للبنين
وزارة التعليم والتعليم العالي - دولة قطر 🇶🇦

---

هذه رسالة تلقائية من نظام إنجاز - يرجى عدم الرد عليها.
"""
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Attach Excel file
        filename = os.path.basename(report_file_path)
        
        with open(report_file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {filename}'
        )
        
        msg.attach(part)
        
        # Send email
        if sender_password:
            # Use SMTP with authentication
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            
            return True, f"✅ تم إرسال التقرير بنجاح إلى {recipient_email}"
        else:
            # No credentials - return message for manual sending
            return False, "⚠️ لم يتم تكوين إعدادات البريد الإلكتروني. يرجى تحميل التقرير وإرساله يدوياً."
    
    except smtplib.SMTPAuthenticationError:
        return False, "❌ خطأ في المصادقة: يرجى التحقق من بيانات الاعتماد"
    
    except smtplib.SMTPException as e:
        return False, f"❌ خطأ في إرسال البريد: {str(e)}"
    
    except Exception as e:
        return False, f"❌ حدث خطأ غير متوقع: {str(e)}"


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not email or '@' not in email:
        return False
    
    parts = email.split('@')
    if len(parts) != 2:
        return False
    
    local, domain = parts
    if not local or not domain or '.' not in domain:
        return False
    
    return True


def get_email_config_instructions() -> str:
    """
    Get instructions for configuring email settings.
    
    Returns:
        str: Configuration instructions in Arabic
    """
    return """
### 📧 تكوين إعدادات البريد الإلكتروني

لتفعيل ميزة إرسال التقارير عبر البريد الإلكتروني، يرجى:

**1. إنشاء متغيرات البيئة:**

في Streamlit Cloud:
- اذهب إلى Settings → Secrets
- أضف المتغيرات التالية:

```toml
ENJAZ_SENDER_EMAIL = "your-email@gmail.com"
ENJAZ_SENDER_PASSWORD = "your-app-password"
```

**2. إعداد Gmail (إذا كنت تستخدم Gmail):**

- اذهب إلى حساب Google
- فعّل التحقق بخطوتين
- أنشئ "كلمة مرور التطبيق" (App Password)
- استخدم كلمة مرور التطبيق في ENJAZ_SENDER_PASSWORD

**3. استخدام خادم SMTP آخر:**

يمكنك استخدام أي خادم SMTP (Outlook, Office365, إلخ) بتعديل الإعدادات في الكود.

---

**ملاحظة:** بدون تكوين الإعدادات، يمكنك تحميل التقرير وإرساله يدوياً.
"""

