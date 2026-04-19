# django_auto_api_gen/generators/project_urls_gen.py
import os
import re

def update_project_urls(app_names, project_urls_path):
    """
    يضيف تلقائيًا أي تطبيق جديد في urlpatterns في ملف urls.py الرئيسي
    دون مسح أي كود موجود مسبقًا
    """
    auto_section_start = "# --- AUTO GENERATED APPS START ---"
    auto_section_end = "# --- AUTO GENERATED APPS END ---"

    existing_content = ""
    if os.path.exists(project_urls_path):
        with open(project_urls_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()

    # إزالة القسم القديم إن وجد
    pattern = re.compile(f"{auto_section_start}.*?{auto_section_end}", re.DOTALL)
    existing_content = pattern.sub("", existing_content).strip()

    # بناء القسم الجديد
    auto_content = auto_section_start + "\n"
    auto_content += "from django.urls import include, path\n"
    auto_content += "try:\n"
    auto_content += "    from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView\n"
    auto_content += "except ImportError:\n"
    auto_content += "    pass\n\n"
    auto_content += "from django_auto_api_gen.views import SystemConfigView\n\n"
    auto_content += "urlpatterns += [\n"
    auto_content += "    # Swagger / OpenAPI Documentation\n"
    auto_content += "    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),\n"
    auto_content += "    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),\n"
    auto_content += "    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),\n"
    auto_content += "    # System Configuration API\n"
    auto_content += "    path('api/system-config/', SystemConfigView.as_view(), name='system-config'),\n\n"
    
    # تطبيقات المشروع
    for app_name in app_names:
        auto_content += f"    path('{app_name}/', include('{app_name}.urls')),\n"
    auto_content += "]\n"
    auto_content += auto_section_end + "\n"

    # دمج المحتوى القديم مع الجديد
    final_content = existing_content + "\n\n" + auto_content if existing_content else auto_content

    with open(project_urls_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"✅ Updated project urls.py safely: {project_urls_path}")
