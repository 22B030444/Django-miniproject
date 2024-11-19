# attendance/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet

# Создаем маршрутизатор и регистрируем AttendanceViewSet
router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet)

# Определяем URL-шаблоны
urlpatterns = [
    path('api/v1/', include(router.urls)),  # Добавляем версию API для лучшей управляемости
]