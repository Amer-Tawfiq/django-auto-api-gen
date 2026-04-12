import os
from django.core.management.base import BaseCommand
from django_auto_api_gen.core import generate_serializers_apis_and_urls_safe

class Command(BaseCommand):
    help = 'توليد تلقائي للـ Serializers والـ APIs والـ URLs والاختبارات لكل تطبيق محدد.'

    def add_arguments(self, parser):
        parser.add_argument('apps', nargs='*', type=str, help='أسماء التطبيقات التي تريد توليد الـ API لها.')
        parser.add_argument('--auth', action='store_true', help='توليد نظام الهوية والمصادقة (Custom User + JWT).')
        parser.add_argument('--settings', type=str, help='مسار إعدادات المشروع (اختياري).')

    def handle(self, *args, **options):
        app_names = options['apps']
        auth_flag = options['auth']
        settings_module = options['settings'] or os.environ.get('DJANGO_SETTINGS_MODULE', 'my_project.settings')

        # نظام الهوية (Identity)
        if auth_flag:
            from django_auto_api_gen.generators.auth_gen import setup_authentication
            from django_auto_api_gen.generators.project_urls_gen import update_project_urls
            
            self.stdout.write(self.style.WARNING("🔐 البدء في إعداد نظام الهوية (users app)..."))
            setup_authentication(app_name='users')
            
            # تحديث urls.py الرئيسي ليشمل الـ users
            project_dir = os.path.dirname(settings_module.replace('.', os.sep) + '.py')
            project_urls_path = os.path.join(project_dir, 'urls.py')
            update_project_urls(['users'], project_urls_path)
            
            self.stdout.write(self.style.SUCCESS("✅ تم إنشاء نظام الهوية بنجاح!"))
            self.stdout.write(self.style.WARNING("\n⚠️  خطوات هامة لإتمام الإعداد في settings.py:"))
            self.stdout.write("1. أضف 'users' و 'rest_framework_simplejwt' إلى INSTALLED_APPS.")
            self.stdout.write("2. أضف AUTH_USER_MODEL = 'users.User'.")
            self.stdout.write("3. تأكد من ضبط REST_FRAMEWORK لاستخدام JWTAuthentication.\n")

        # توليد الـ APIs للتطبيقات المحددة
        if app_names:
            self.stdout.write(self.style.SUCCESS(f"🚀 البدء في معالجة التطبيقات: {', '.join(app_names)}"))
            try:
                generate_serializers_apis_and_urls_safe(app_names, settings_module)
                self.stdout.write(self.style.SUCCESS("✨ تم الانتهاء من التوليد بنجاح!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ حدث خطأ أثناء التوليد: {e}"))
        elif not auth_flag:
            self.stdout.write(self.style.ERROR("❌ يرجى تحديد اسم تطبيق أو استخدام خيار --auth"))
