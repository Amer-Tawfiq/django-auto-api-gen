import os
import django
import importlib
import pkgutil
from django.apps import apps

def setup_django(project_settings_module):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", project_settings_module)
    django.setup()

def load_models_from_app(app_name):
    """تحميل الموديلات من app معين (حتى لو داخل مجلد models)"""
    try:
        models_package_name = f"{app_name}.models"
        models_package = importlib.import_module(models_package_name)
        for loader, mod_name, is_pkg in pkgutil.iter_modules(models_package.__path__):
            importlib.import_module(f"{models_package_name}.{mod_name}")
    except ModuleNotFoundError:
        pass

    try:
        return list(apps.get_app_config(app_name).get_models())
    except LookupError:
        print(f"⚠️ App {app_name} not found or not in INSTALLED_APPS")
        return []

def format_code(directory_path):
    """تنسيق الكود المولد باستخدام أداة black"""
    import subprocess
    import sys
    try:
        print(f"✨ Formatting code in {directory_path}...")
        subprocess.run([sys.executable, "-m", "black", directory_path], check=False, capture_output=True)
    except Exception as e:
        print(f"⚠️ Could not format code: {e}")
