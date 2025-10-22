# 🚀 دليل النشر - نظام إنجاز

## نظرة عامة

هذا الدليل يشرح كيفية نشر تطبيق **إنجاز** على منصات مختلفة.

## النشر المحلي (Local Deployment)

### المتطلبات
- Python 3.11 أو أحدث
- pip3
- نظام التشغيل: Windows, macOS, أو Linux

### الخطوات

1. **تحميل المشروع**
```bash
# إذا كان لديك git
git clone <repository-url>
cd enjaz

# أو قم بفك ضغط ملف ZIP
unzip enjaz.zip
cd enjaz
```

2. **إنشاء بيئة افتراضية (اختياري ولكن موصى به)**
```bash
# على Windows
python -m venv venv
venv\Scripts\activate

# على macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **تثبيت المتطلبات**
```bash
pip3 install -r requirements.txt
```

4. **تشغيل التطبيق**
```bash
streamlit run app.py
```

5. **الوصول إلى التطبيق**
افتح المتصفح على: `http://localhost:8501`

## النشر على Streamlit Cloud

### المتطلبات
- حساب GitHub
- حساب Streamlit Cloud (مجاني)

### الخطوات

1. **رفع المشروع إلى GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **الاتصال بـ Streamlit Cloud**
- اذهب إلى: https://share.streamlit.io
- سجّل الدخول باستخدام حساب GitHub
- انقر على "New app"

3. **تكوين التطبيق**
- Repository: اختر مستودع GitHub الخاص بك
- Branch: main
- Main file path: app.py
- انقر على "Deploy"

4. **الوصول إلى التطبيق**
سيتم إعطاؤك رابط مثل: `https://your-app-name.streamlit.app`

## النشر على خادم Linux

### المتطلبات
- خادم Linux (Ubuntu 20.04+ موصى به)
- صلاحيات sudo
- اتصال بالإنترنت

### الخطوات

1. **تحديث النظام**
```bash
sudo apt update
sudo apt upgrade -y
```

2. **تثبيت Python 3.11**
```bash
sudo apt install python3.11 python3.11-venv python3-pip -y
```

3. **نقل المشروع إلى الخادم**
```bash
# استخدم scp أو git clone
scp -r enjaz user@server:/home/user/
# أو
git clone <repository-url> /home/user/enjaz
```

4. **تثبيت المتطلبات**
```bash
cd /home/user/enjaz
pip3 install -r requirements.txt
```

5. **إنشاء خدمة systemd (للتشغيل التلقائي)**
```bash
sudo nano /etc/systemd/system/enjaz.service
```

أضف المحتوى التالي:
```ini
[Unit]
Description=Enjaz Streamlit Application
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/user/enjaz
ExecStart=/usr/bin/python3.11 -m streamlit run app.py --server.port=8501 --server.headless=true
Restart=always

[Install]
WantedBy=multi-user.target
```

6. **تفعيل وبدء الخدمة**
```bash
sudo systemctl daemon-reload
sudo systemctl enable enjaz
sudo systemctl start enjaz
sudo systemctl status enjaz
```

7. **تكوين Nginx (اختياري)**

إذا كنت تريد استخدام اسم نطاق:

```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/enjaz
```

أضف:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

تفعيل التكوين:
```bash
sudo ln -s /etc/nginx/sites-available/enjaz /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## النشر باستخدام Docker

### إنشاء Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]
```

### بناء وتشغيل الحاوية

```bash
# بناء الصورة
docker build -t enjaz-app .

# تشغيل الحاوية
docker run -d -p 8501:8501 --name enjaz enjaz-app

# عرض السجلات
docker logs -f enjaz
```

## النشر على Heroku

### المتطلبات
- حساب Heroku
- Heroku CLI

### الخطوات

1. **إنشاء ملف setup.sh**
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

2. **إنشاء Procfile**
```
web: sh setup.sh && streamlit run app.py
```

3. **النشر**
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku open
```

## تكوين المتغيرات البيئية

إذا كنت بحاجة إلى متغيرات بيئية (مثل مفاتيح API):

### Streamlit Cloud
- اذهب إلى App settings > Secrets
- أضف المتغيرات بصيغة TOML

### Linux Server
```bash
# في ملف .env
export API_KEY="your-key"
export DATABASE_URL="your-url"

# تحميل المتغيرات
source .env
```

### Docker
```bash
docker run -d -p 8501:8501 \
  -e API_KEY="your-key" \
  -e DATABASE_URL="your-url" \
  --name enjaz enjaz-app
```

## الأمان والأفضليات

### 1. تحديث المكتبات بانتظام
```bash
pip3 install --upgrade -r requirements.txt
```

### 2. استخدام HTTPS
- احصل على شهادة SSL من Let's Encrypt
- استخدم Nginx أو Caddy كوكيل عكسي

### 3. تقييد الوصول
- استخدم جدار ناري (firewall)
- قيّد الوصول إلى عناوين IP محددة إذا لزم الأمر

### 4. النسخ الاحتياطي
```bash
# نسخ احتياطي للمشروع
tar -czf enjaz-backup-$(date +%Y%m%d).tar.gz /home/user/enjaz

# نسخ احتياطي للبيانات (إذا كان هناك قاعدة بيانات)
# أضف أوامر النسخ الاحتياطي المناسبة
```

## المراقبة والصيانة

### عرض السجلات

**Systemd:**
```bash
sudo journalctl -u enjaz -f
```

**Docker:**
```bash
docker logs -f enjaz
```

**Streamlit Cloud:**
- اذهب إلى App settings > Logs

### إعادة التشغيل

**Systemd:**
```bash
sudo systemctl restart enjaz
```

**Docker:**
```bash
docker restart enjaz
```

**Streamlit Cloud:**
- انقر على "Reboot app" في لوحة التحكم

## استكشاف الأخطاء

### المشكلة: التطبيق لا يبدأ
**الحل:**
```bash
# تحقق من السجلات
sudo journalctl -u enjaz -n 50

# تحقق من المتطلبات
pip3 list | grep streamlit

# تحقق من المنفذ
sudo netstat -tulpn | grep 8501
```

### المشكلة: خطأ في الذاكرة
**الحل:**
- زيادة ذاكرة الخادم
- تحسين الكود لتقليل استخدام الذاكرة
- استخدام caching في Streamlit

### المشكلة: بطء التطبيق
**الحل:**
- استخدم `@st.cache_data` للبيانات
- استخدم `@st.cache_resource` للموارد
- قلل حجم البيانات المُحمّلة

## الدعم

للمساعدة في النشر:
- **البريد الإلكتروني**: Sahar.Osman@education.qa
- **التوثيق الرسمي**: https://docs.streamlit.io/

---

© 2025 — جميع الحقوق محفوظة | مدرسة عثمان بن عفّان النموذجية للبنين

