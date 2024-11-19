# users/urls.py

from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import RegistrationView

# Настройка схемы Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Student Management System API",
        default_version='v1',
        description="API documentation for user registration and authentication.",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@studentms.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Эндпоинт регистрации пользователей
    path('register/', RegistrationView.as_view(), name='register'),

    # Эндпоинты аутентификации (Djoser)
    path('auth/', include('djoser.urls')),  # Эндпоинты для аутентификации
    path('auth/', include('djoser.urls.jwt')),  # Эндпоинты для JWT аутентификации

    # Swagger UI для документации API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
]