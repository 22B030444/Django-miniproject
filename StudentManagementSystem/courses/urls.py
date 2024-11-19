# courses/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, EnrollmentViewSet

# Настройка DefaultRouter для курсов и зачислений
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollments')

urlpatterns = [
    path('api/v1/', include(router.urls)),  # Версия 1 API
]