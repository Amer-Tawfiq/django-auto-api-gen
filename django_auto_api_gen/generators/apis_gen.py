import os
import textwrap

def generate_apis(app_name, models):
    api_dir = os.path.join(app_name, 'apis')
    os.makedirs(api_dir, exist_ok=True)

    init_file = os.path.join(api_dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write("# Auto-generated api package\n")

    imports = []
    registrations = []

    for model in models:
        model_name = model.__name__
        api_file = os.path.join(api_dir, f"{model_name}.py")

        # تحليل الحقول للفلترة والبحث والترتيب
        filter_fields = []
        search_fields = []
        ordering_fields = ['id']
        select_related = []
        prefetch_related = []

        for field in model._meta.get_fields():
            if not field.concrete and not field.is_relation:
                continue
            
            field_name = field.name
            
            # التعامل مع العلاقات
            if field.is_relation:
                if field.many_to_one or field.one_to_one:
                    filter_fields.append(field_name)
                    select_related.append(field_name)
                elif field.many_to_many or field.one_to_many:
                    prefetch_related.append(field_name)
                continue

            # الحقول العادية
            internal_type = field.get_internal_type()
            
            if internal_type in ['CharField', 'TextField']:
                search_fields.append(field_name)
            
            if internal_type in ['IntegerField', 'FloatField', 'DecimalField', 'BooleanField', 'DateField', 'DateTimeField']:
                filter_fields.append(field_name)
            
            if internal_type in ['IntegerField', 'FloatField', 'DecimalField', 'DateField', 'DateTimeField', 'AutoField']:
                ordering_fields.append(field_name)

        # بناء الاستعلام المحسن
        qs_code = f"{model_name}.objects.all()"
        if select_related:
            sel_related_str = "', '".join(select_related)
            qs_code += f".select_related('{sel_related_str}')"
        if prefetch_related:
            pre_related_str = "', '".join(prefetch_related)
            qs_code += f".prefetch_related('{pre_related_str}')"

        if not os.path.exists(api_file):
            content = textwrap.dedent(f"""\
                from rest_framework.viewsets import ModelViewSet
                from rest_framework.filters import SearchFilter, OrderingFilter
                from django_filters.rest_framework import DjangoFilterBackend
                from ..models.{model_name} import {model_name}
                from ..serializers.{model_name} import {model_name}Serializer

                class {model_name}MVS(ModelViewSet):
                    queryset = {qs_code}
                    serializer_class = {model_name}Serializer
                    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
                    filterset_fields = {filter_fields}
                    search_fields = {search_fields}
                    ordering_fields = {ordering_fields}
                    ordering = ['id']
            """)
            with open(api_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Created api: {api_file}")

        imports.append(f"from .apis.{model_name} import {model_name}MVS")
        registrations.append(f"router.register('{model_name.lower()}', {model_name}MVS)")

    return imports, registrations
