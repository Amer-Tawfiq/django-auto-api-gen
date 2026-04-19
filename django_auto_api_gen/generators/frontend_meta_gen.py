import json
import os
from .urls_gen import camel_to_kebab

def generate_frontend_meta(app_names, models_dict, project_root):
    """
    توليد ملف JSON يحتوي على إعدادات الشاشات للفرونت إند.
    
    app_names: قائمة بأسماء التطبيقات.
    models_dict: قاموس {app_name: [list_of_models]}.
    project_root: المسار الرئيسي للمشروع لحفظ الملف العالمي.
    """
    all_screens = []
    screen_order = 1

    for app_name, models in models_dict.items():
        # الأب هو اسم التطبيق (يمكن تخصيصه لاحقاً)
        parent_screen = app_name.capitalize()

        for model in models:
            model_name = model.__name__
            verbose_name_ar = getattr(model._meta, 'verbose_name', model_name)
            
            # تحويل اسم المودل إلى kebab-case للروابط والأبي آي
            kebab_name = camel_to_kebab(model_name)
            
            screen_data = {
                "name_ar": str(verbose_name_ar),
                "name_en": model_name,
                "order": screen_order,
                "parent_screen": parent_screen,
                "screen_type": "CRUD",
                "router": f"/{app_name}/{kebab_name}",
                "api_endpoint": f"/api/{app_name}/{kebab_name}/",
                "model_name": model_name,
                "viewset_class": f"{model_name}MVS",
                "fields": []
            }

            # استخراج الحقول
            for field in model._meta.get_fields():
                if not field.concrete and not field.is_relation:
                    continue
                
                # تخطي حقول العلاقات العكسية
                if field.one_to_many or field.many_to_many:
                    continue

                field_info = {
                    "name": field.name,
                    "label": str(getattr(field, 'verbose_name', field.name)),
                    "type": field.get_internal_type(),
                    "group": "البيانات الأساسية",
                    "required": not getattr(field, 'blank', False),
                    "is_relation": field.is_relation
                }
                
                if field.is_relation and field.related_model:
                    field_info["related_model"] = field.related_model.__name__

                screen_data["fields"].append(field_info)

            all_screens.append(screen_data)
            screen_order += 1

    # حفظ الملف في المجلد الرئيسي للمشروع
    output_path = os.path.join(project_root, 'global_screens_config.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"screens": all_screens}, f, ensure_ascii=False, indent=4)

    print(f"✅ Generated global frontend config: {output_path}")
    return output_path
