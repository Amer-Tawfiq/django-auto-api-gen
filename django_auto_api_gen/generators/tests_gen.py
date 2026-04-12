import os
import textwrap
from .urls_gen import camel_to_kebab

def generate_tests(app_name, models):
    # --- مجلد tests ---
    tests_dir = os.path.join(app_name, 'tests')
    os.makedirs(tests_dir, exist_ok=True)
    
    init_file = os.path.join(tests_dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write("# Auto-generated tests package\n")
            
    for model in models:
        model_name = model.__name__
        test_file = os.path.join(tests_dir, f"test_{model_name.lower()}_api.py")
        url_route_name = camel_to_kebab(model_name)
        
        if not os.path.exists(test_file):
            # محاولة تخمين بيانات وهمية بسيطة لعمليات الـ POST و PUT
            post_data = {}
            for field in model._meta.get_fields():
                if field.concrete and not field.is_relation and not field.auto_created:
                    internal_type = field.get_internal_type()
                    if internal_type in ['CharField', 'TextField']:
                        post_data[field.name] = "test_data"
                    elif internal_type in ['IntegerField', 'FloatField', 'DecimalField']:
                        post_data[field.name] = 1
                    elif internal_type == 'BooleanField':
                        post_data[field.name] = True

            content = textwrap.dedent(f"""\
                from rest_framework.test import APITestCase
                from django.urls import reverse
                from rest_framework import status
                from ..models.{model_name} import {model_name}

                class {model_name}APITestCase(APITestCase):
                    def setUp(self):
                        # استخدام kebab-case للمسارات كما هو متبع في urls_gen
                        self.url = reverse('{url_route_name}-list')
                        self.sample_data = {post_data}
                        # إنشاء كائن لاستخدامه في اختبارات الـ Retrieve و Update و Delete
                        # ملاحظة: قد تحتاج لتعديل البيانات يدوياً إذا كان هناك متطلبات خاصة (مثل حقول فريدة)
                        self.model_obj = {model_name}.objects.create(**self.sample_data)
                    
                    def test_list_{model_name.lower()}(self):
                        response = self.client.get(self.url)
                        self.assertEqual(response.status_code, status.HTTP_200_OK)

                    def test_retrieve_{model_name.lower()}(self):
                        url = reverse('{url_route_name}-detail', args=[self.model_obj.id])
                        response = self.client.get(url)
                        self.assertEqual(response.status_code, status.HTTP_200_OK)

                    def test_create_{model_name.lower()}(self):
                        data = self.sample_data.copy()
                        # تعديل بسيط لتجنب تعارض الـ Unique إن وجد
                        for key in data:
                            if isinstance(data[key], str):
                                data[key] = data[key] + "_new"
                        
                        response = self.client.post(self.url, data)
                        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

                    def test_update_{model_name.lower()}(self):
                        url = reverse('{url_route_name}-detail', args=[self.model_obj.id])
                        data = self.sample_data.copy()
                        response = self.client.put(url, data)
                        self.assertEqual(response.status_code, status.HTTP_200_OK)

                    def test_delete_{model_name.lower()}(self):
                        url = reverse('{url_route_name}-detail', args=[self.model_obj.id])
                        response = self.client.delete(url)
                        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            """)
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Created test: {test_file}")
