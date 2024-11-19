from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet

# Create a router and register the AttendanceViewSet
router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet)

# Define the URL patterns
urlpatterns = [
    path('api/', include(router.urls)),  # Prefix the attendance endpoints with 'api/'
]
