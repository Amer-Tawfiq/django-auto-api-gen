# Django Auto API Gen

`django-auto-api-gen` هي أداة لتوليد **Django REST Framework (DRF) serializers** و **API ViewSets** و **URLs** و **Tests** تلقائيًا لكل النماذج (`models`) الموجودة في تطبيقات Django المحددة.  

تم تصميم هذه الأداة لتوفير الوقت وتقليل الكود المكرر في مشاريع Django، خصوصًا عند التعامل مع عدد كبير من النماذج.

---

## 🚀 المميزات الاحترافية

- **أمر إدارة Django:** توليد كل شيء بـ `python manage.py generate_api`.
- **توليد تلقائي للـ serializers:** مع دعم الـ Nesting (depth=1).
- **توليد تلقائي للـ API ViewSets:** مع دعم البحث والفلترة والترتيب تلقائياً.
- **تحسين الاستعلامات:** استخدام `select_related` و `prefetch_related` تلقائياً.
- **اختبارات وحدة جاهزة:** توليد اختبارات API (CRUD) لكل نموذج للتأكد من سلامة الكود.
- **توثيق Swagger:** دعم تلقائي لـ Swagger و Redoc عبر `drf-spectacular`.

---

## ⚡️ كيفية الاستخدام

1. **تثبيت الحزمة:**

```bash
pip install git+https://github.com/Amer-Tawfiq/django-auto-api-gen.git
```

2. **الإعداد (Settings):**
أضف `django_auto_api_gen` و `drf_spectacular` إلى قائمة الـ `INSTALLED_APPS` في ملف `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'django_auto_api_gen',
    'drf_spectacular',
    ...
]

# إعدادات التوثيق
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

3. **التوليد التلقائي (Generation):**
الآن يمكنك توليد كل شيء بضغطة زر واحدة:

```bash
# لتوليد الـ API لتطبيقات معينة
python manage.py generate_api app1 app2

# لتوليد نظام الهوية والمصادقة (User Auth + JWT)
python manage.py generate_api --auth
```

سيقوم هذا الأمر بإنشاء:
- **نظام مستخدمين متكامل** (عند استخدام --auth): Custom User, Login, Register, Profile, JWT.
- **Serializers** لكل النماذج (مع `depth=1`).
- **APIs (ViewSets)** مع الفلترة والبحث والترتيب.
- **URLs** مرتبطة تلقائياً في التطبيق والمشروع.
- **Tests** اختبارات وحدة جاهزة للتشغيل.

---

## 🧪 تشغيل الاختبارات

بعد التوليد، يمكنك التأكد من عمل الـ API بشكل سليم عبر تشغيل:

```bash
python manage.py test
```

---

## 📖 التوثيق (Swagger)

بمجرد تشغيل السيرفر، يمكنك الوصول للتوثيق عبر الروابط التالية:
- **Swagger UI**: `http://127.0.0.1:8000/api/docs/`
- **ReDoc**: `http://127.0.0.1:8000/api/redoc/`