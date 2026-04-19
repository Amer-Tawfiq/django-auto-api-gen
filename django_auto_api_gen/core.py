from .generators.utils import setup_django, load_models_from_app, format_code
from .generators.serializers_gen import generate_serializers
from .generators.apis_gen import generate_apis
from .generators.urls_gen import update_urls
from .generators.project_urls_gen import update_project_urls
from .generators.tests_gen import generate_tests
from .generators.base_serializer_gen import generate_base_serializer
from .generators.readme_gen import generate_app_readme
from .generators.frontend_meta_gen import generate_frontend_meta
import os

def generate_serializers_apis_and_urls_safe(app_names, project_settings_module='my_project.settings'):
    setup_django(project_settings_module)

    for app_name in app_names:
        print(f"🚀 Processing app: {app_name}")
        models = load_models_from_app(app_name)
        if not models:
            continue

        generate_base_serializer(app_name)
        generate_serializers(app_name, models)
        imports, registrations = generate_apis(app_name, models)
        update_urls(app_name, imports, registrations)
        generate_tests(app_name, models)
        generate_app_readme(app_name, models)
        
        # تنسيق كود التطبيق
        format_code(app_name)

    # توليد ملف الإعدادات الموحد للفرونت إند
    project_root = os.getcwd()
    models_dict = {app: load_models_from_app(app) for app in app_names}
    generate_frontend_meta(app_names, models_dict, project_root)

     # تحديث urls.py الرئيسي بجانب settings
    project_dir = os.path.dirname(project_settings_module.replace('.', os.sep) + '.py')
    project_urls_path = os.path.join(project_dir, 'urls.py')
    update_project_urls(app_names, project_urls_path)
    
    # تنسيق مجلد المشروع الرئيسي
    format_code(project_dir)

    print(" Done generating serializers, apis, and urls safely.")
