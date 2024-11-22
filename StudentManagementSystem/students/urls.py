from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from students.views import StudentViewSet

# Router configuration
router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='students')

# Swagger Schema
schema_view = get_schema_view(
    openapi.Info(
        title="Student Management System API",
        default_version='v1',
        description="API documentation for managing students and admin operations.",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@studentms.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
    path('api/v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),
]