import os
import re

def camel_to_kebab(name):
    """
    يحول الاسم من CamelCase إلى kebab-case
    مثال: BusStudent -> bus-student
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    kebab = re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()
    return kebab


def update_urls(app_name, imports, registrations):
    """
    تحديث urls.py داخل التطبيق بطريقة آمنة،
    مع تحويل أسماء النماذج إلى kebab-case عند التسجيل.
    """
    urls_file = os.path.join(app_name, 'urls.py')
    auto_section_start = "# --- AUTO GENERATED START ---"
    auto_section_end = "# --- AUTO GENERATED END ---"

    existing_content = ""
    if os.path.exists(urls_file):
        with open(urls_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()

    # إزالة القسم القديم إذا كان موجود
    pattern = re.compile(f"{auto_section_start}.*?{auto_section_end}", re.DOTALL)
    existing_content = pattern.sub("", existing_content).strip()

    # بناء القسم الجديد
    auto_content = auto_section_start + "\nfrom rest_framework.routers import DefaultRouter\n\nrouter = DefaultRouter()\n\n"
    
    # إضافة الاستيرادات
    for imp in imports:
        auto_content += imp + "\n"
    auto_content += "\n"

    # إضافة التسجيلات مع تحويل إلى kebab-case
    for reg in registrations:
        # استخراج اسم الـ model من النص الأصلي: 'router.register('name', ViewSet)'
        match = re.match(r"router\.register\('(.+?)',\s*(.+?)\)", reg)
        if match:
            model_class = match.group(2)  # اسم الـ ViewSet
            model_name = re.sub(r'MVS$', '', model_class)  # إزالة MVS للحصول على اسم النموذج
            url_name = camel_to_kebab(model_name)
            auto_content += f"router.register('{url_name}', {model_class})\n"

    auto_content += "\nurlpatterns = router.urls\n" + auto_section_end + "\n"

    # دمج المحتوى القديم مع الجديد
    final_content = existing_content + "\n\n" + auto_content if existing_content else auto_content

    with open(urls_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Updated urls.py safely: {urls_file}")
