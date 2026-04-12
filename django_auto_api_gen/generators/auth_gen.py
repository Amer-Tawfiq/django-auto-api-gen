import os
import textwrap

def setup_authentication(app_name='users'):
    """
    يقوم بإنشاء تطبيق هوية كامل (Identity & Auth) باستخدام Custom User و SimpleJWT.
    """
    # --- مجلد التطبيق ---
    os.makedirs(app_name, exist_ok=True)
    
    # --- بناء الهيكل الشجري للمجلدات ---
    sub_packages = ['models', 'serializers', 'api']
    for sub in sub_packages:
        path = os.path.join(app_name, sub)
        os.makedirs(path, exist_ok=True)
        init_file = os.path.join(path, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w', encoding='utf-8') as f:
                 f.write(f"# Auto-generated {sub} package\n")

    # --- User Model ---
    model_file = os.path.join(app_name, 'models', 'User.py')
    if not os.path.exists(model_file):
        with open(model_file, 'w', encoding='utf-8') as f:
            f.write(textwrap.dedent("""\
                from django.contrib.auth.models import AbstractUser
                from django.db import models

                class User(AbstractUser):
                    \"\"\"
                    Custom User model for future flexibility.
                    \"\"\"
                    def __str__(self):
                        return self.username
            """))
        
        # إضافة الموديل لـ __init__.py الخاص بـ models
        with open(os.path.join(app_name, 'models', '__init__.py'), 'a', encoding='utf-8') as f:
            f.write("from .User import User\n")

    # --- Serializers ---
    serializer_file = os.path.join(app_name, 'serializers', 'UserSerializer.py')
    if not os.path.exists(serializer_file):
        with open(serializer_file, 'w', encoding='utf-8') as f:
            f.write(textwrap.dedent(f"""\
                from rest_framework import serializers
                from ..models.User import User

                class UserSerializer(serializers.ModelSerializer):
                    class Meta:
                        model = User
                        fields = ('id', 'username', 'email', 'first_name', 'last_name')

                class RegisterSerializer(serializers.ModelSerializer):
                    password = serializers.CharField(write_only=True)

                    class Meta:
                        model = User
                        fields = ('username', 'password', 'email', 'first_name', 'last_name')

                    def create(self, validated_data):
                        user = User.objects.create_user(**validated_data)
                        return user
            """))

    # --- API Views ---
    api_file = os.path.join(app_name, 'api', 'AuthViews.py')
    if not os.path.exists(api_file):
        with open(api_file, 'w', encoding='utf-8') as f:
            f.write(textwrap.dedent(f"""\
                from rest_framework import generics, permissions
                from rest_framework.response import Response
                from ..serializers.UserSerializer import UserSerializer, RegisterSerializer
                from ..models.User import User

                class RegisterAPIView(generics.CreateAPIView):
                    \"\"\"
                    API لتسجيل مستخدم جديد.
                    \"\"\"
                    queryset = User.objects.all()
                    permission_classes = (permissions.AllowAny,)
                    serializer_class = RegisterSerializer

                class ProfileAPIView(generics.RetrieveUpdateAPIView):
                    \"\"\"
                    API لعرض وتعديل الملف الشخصي للمستخدم الحالي.
                    \"\"\"
                    serializer_class = UserSerializer
                    permission_classes = (permissions.IsAuthenticated,)

                    def get_object(self):
                        return self.request.user
            """))

    # --- URLs ---
    url_file = os.path.join(app_name, 'urls.py')
    if not os.path.exists(url_file):
        with open(url_file, 'w', encoding='utf-8') as f:
            f.write(textwrap.dedent(f"""\
                from django.urls import path
                from rest_framework_simplejwt.views import (
                    TokenObtainPairView,
                    TokenRefreshView,
                )
                from .api.AuthViews import RegisterAPIView, ProfileAPIView

                urlpatterns = [
                    # تسجيل حساب جديد
                    path('register/', RegisterAPIView.as_view(), name='auth_register'),
                    # تسجيل الدخول والحصول على التوكن
                    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                    # تحديث التوكن (Refresh)
                    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                    # بيانات الملف الشخصي
                    path('profile/', ProfileAPIView.as_view(), name='auth_profile'),
                ]
            """))
    
    print(f"✅ Identity system (users app) setup successfully!")
