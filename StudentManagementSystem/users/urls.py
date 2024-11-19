from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import RegistrationView

# Swagger Schema Configuration
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
    # User Registration
    path('register/', RegistrationView.as_view(), name='register'),

    # Authentication Endpoints (Djoser)
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
]
