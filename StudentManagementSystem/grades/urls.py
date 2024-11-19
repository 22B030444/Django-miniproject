# grades/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GradeViewSet

# Создаем маршрутизатор и регистрируем GradeViewSet
router = DefaultRouter()
router.register(r'grades', GradeViewSet)

# Определяем URL-шаблоны
urlpatterns = [
    path('api/v1/', include(router.urls)),  # Добавляем версию API для лучшей управляемости
]