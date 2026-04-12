import os
import textwrap

def generate_base_serializer(app_name):
    """
    إنشاء الكلاس الأساسي للـ Serializers الذي يدعم الحقول الديناميكية داخل التطبيق المحددة.
    """
    serializers_dir = os.path.join(app_name, 'serializers')
    os.makedirs(serializers_dir, exist_ok=True)
    
    base_file = os.path.join(serializers_dir, 'base.py')
    if not os.path.exists(base_file):
        content = textwrap.dedent("""
            from rest_framework import serializers

            class DynamicFieldsModelSerializer(serializers.ModelSerializer):
                \"\"\"
                Serializer يسمح بتحديد الحقول المطلوبة عبر query parameter: ?fields=id,name
                \"\"\"
                def __init__(self, *args, **kwargs):
                    # إزالة 'fields' من kwargs قبل تمريره للسوبر
                    fields = kwargs.pop('fields', None)

                    super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

                    if fields is None and 'request' in self.context:
                        # محاولة الحصول على الحقول من query parameters
                        fields_param = self.context['request'].query_params.get('fields')
                        if fields_param:
                            fields = fields_param.split(',')

                    if fields is not None:
                        # حذف أي حقول غير مطلوبة
                        allowed = set(fields)
                        existing = set(self.fields)
                        for field_name in existing - allowed:
                            self.fields.pop(field_name)
        """).lstrip()
        with open(base_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created base serializer: {base_file}")
