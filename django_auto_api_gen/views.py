import os
import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SystemConfigView(APIView):
    """
    API لاسترجاع إعدادات الشاشات المولدة تلقائياً.
    """
    permission_classes = []  # يمكن تعديلها لاحقاً حسب الحاجة
    
    def get(self, request, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'global_screens_config.json')
        
        if not os.path.exists(file_path):
            return Response(
                {"error": "Global screens configuration file not found. Please run generate_api command first."},
                status=status.HTTP_404_NOT_FOUND
            )
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Response(data)
        except Exception as e:
            return Response(
                {"error": f"Failed to read configuration: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
