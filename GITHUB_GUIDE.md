# 📘 دليل رفع المشروع على GitHub

## الخطوات التفصيلية

### 1️⃣ إنشاء حساب GitHub (إذا لم يكن لديك)

1. اذهب إلى https://github.com
2. انقر على "Sign up"
3. أدخل البريد الإلكتروني وكلمة المرور
4. أكمل عملية التسجيل

### 2️⃣ إنشاء Repository جديد

1. بعد تسجيل الدخول، انقر على "+" في الأعلى
2. اختر "New repository"
3. املأ المعلومات:
   - **Repository name**: `enjaz` (أو أي اسم تفضله)
   - **Description**: `نظام إنجاز لتحليل التقييمات الأسبوعية - Enjaz Assessment Analysis System`
   - **Visibility**: اختر Public أو Private
   - **لا تختر** "Initialize this repository with a README" (لأن لدينا ملفات جاهزة)
4. انقر على "Create repository"

### 3️⃣ ربط المشروع المحلي بـ GitHub

بعد إنشاء الـ repository، ستظهر لك صفحة بها تعليمات. استخدم هذه الأوامر:

```bash
cd /path/to/enjaz

# إضافة remote (استبدل YOUR-USERNAME باسم المستخدم الخاص بك)
git remote add origin https://github.com/YOUR-USERNAME/enjaz.git

# التحقق من الـ remote
git remote -v

# رفع الملفات إلى GitHub
git push -u origin main
```

### 4️⃣ إدخال بيانات الاعتماد

عند تنفيذ `git push`، سيطلب منك:
- **Username**: اسم المستخدم في GitHub
- **Password**: استخدم **Personal Access Token** (وليس كلمة المرور العادية)

#### كيفية إنشاء Personal Access Token:

1. اذهب إلى GitHub → Settings (من القائمة المنسدلة في الأعلى)
2. في القائمة الجانبية، اختر "Developer settings"
3. اختر "Personal access tokens" → "Tokens (classic)"
4. انقر على "Generate new token" → "Generate new token (classic)"
5. أدخل اسماً للـ token (مثل: "Enjaz Project")
6. اختر الصلاحيات:
   - ✅ `repo` (جميع الصلاحيات)
7. انقر على "Generate token"
8. **انسخ الـ token فوراً** (لن تتمكن من رؤيته مرة أخرى!)
9. استخدم هذا الـ token كـ "password" عند تنفيذ `git push`

### 5️⃣ التحقق من الرفع

بعد نجاح `git push`:
1. اذهب إلى https://github.com/YOUR-USERNAME/enjaz
2. يجب أن ترى جميع الملفات

## الأوامر الأساسية

### رفع تعديلات جديدة

```bash
# إضافة الملفات المعدلة
git add .

# عمل commit
git commit -m "وصف التعديلات"

# رفع إلى GitHub
git push origin main
```

### سحب آخر التحديثات

```bash
git pull origin main
```

### عرض الحالة

```bash
git status
```

### عرض السجل

```bash
git log --oneline
```

## النشر على Streamlit Cloud

بعد رفع المشروع على GitHub، يمكنك نشره مجاناً على Streamlit Cloud:

### الخطوات:

1. **اذهب إلى**: https://share.streamlit.io
2. **سجّل الدخول** باستخدام حساب GitHub
3. **انقر على** "New app"
4. **املأ المعلومات**:
   - **Repository**: اختر `YOUR-USERNAME/enjaz`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. **انقر على** "Deploy"
6. **انتظر** بضع دقائق حتى يكتمل النشر
7. **احصل على الرابط** مثل: `https://your-app-name.streamlit.app`

### ملاحظات مهمة:

- التطبيق سيُعاد نشره تلقائياً عند كل `git push`
- يمكنك إيقاف أو حذف التطبيق من لوحة التحكم
- الخدمة مجانية للمشاريع العامة

## حل المشاكل الشائعة

### المشكلة: "Authentication failed"

**الحل**: تأكد من استخدام Personal Access Token وليس كلمة المرور العادية.

### المشكلة: "Permission denied"

**الحل**: تأكد من أن لديك صلاحيات الكتابة على الـ repository.

### المشكلة: "fatal: remote origin already exists"

**الحل**:
```bash
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/enjaz.git
```

### المشكلة: "Your branch is ahead of 'origin/main'"

**الحل**:
```bash
git push origin main
```

## نصائح

### ✅ أفضل الممارسات

1. **Commit بانتظام**: لا تنتظر حتى تجمع تعديلات كثيرة
2. **رسائل واضحة**: استخدم رسائل commit وصفية
3. **اختبر قبل الـ push**: تأكد من أن الكود يعمل
4. **استخدم .gitignore**: لا ترفع ملفات غير ضرورية

### 📝 أمثلة على رسائل Commit جيدة

```bash
git commit -m "إضافة: ميزة تصدير PDF للتقارير"
git commit -m "إصلاح: خطأ في حساب نسب الإكمال"
git commit -m "تحديث: تحسين واجهة لوحة المعلومات"
git commit -m "توثيق: إضافة أمثلة في README"
```

### 🔒 الأمان

- **لا ترفع** ملفات تحتوي على كلمات مرور أو مفاتيح API
- **استخدم** `.gitignore` لاستبعاد الملفات الحساسة
- **راجع** الملفات قبل الـ commit

## الموارد المفيدة

- **توثيق Git**: https://git-scm.com/doc
- **توثيق GitHub**: https://docs.github.com
- **توثيق Streamlit Cloud**: https://docs.streamlit.io/streamlit-community-cloud

## الدعم

للمساعدة:
- **البريد الإلكتروني**: Sahar.Osman@education.qa
- **GitHub Issues**: أنشئ issue في الـ repository

---

**رؤيتنا**: "متعلم ريادي لتنمية مستدامة"

© 2025 — مدرسة عثمان بن عفّان النموذجية للبنين

