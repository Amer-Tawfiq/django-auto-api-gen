
import os
import textwrap

def generate_serializers(app_name, app_models):
    # --- مجلد serializers ---
        serializers_dir = os.path.join(app_name, 'serializers')
        os.makedirs(serializers_dir, exist_ok=True)
        init_file = os.path.join(serializers_dir, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w', encoding='utf-8') as f:
                  f.write("# Auto-generated serializers package\n")
        
        for model in app_models:
            model_name = model.__name__

            # Check for relations (ForeignKey, ManyToMany, etc.)
            has_relations = any(field.is_relation for field in model._meta.get_fields())
            depth_str = "\n        depth = 1" if has_relations else ""

            # --- serializer ---
            serializer_file = os.path.join(serializers_dir, f"{model_name}.py")
            if not os.path.exists(serializer_file):
                serializer_content = textwrap.dedent(f"""\
                    from rest_framework import serializers
                    from .base import DynamicFieldsModelSerializer
                    from ..models.{model_name} import {model_name}

                    class {model_name}Serializer(DynamicFieldsModelSerializer):
                        class Meta:
                            model = {model_name}
                            fields = '__all__'{depth_str}
                """)
                with open(serializer_file, 'w', encoding='utf-8') as f:
                    f.write(serializer_content)
                print(f"Created serializer: {serializer_file}")