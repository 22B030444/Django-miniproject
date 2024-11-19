from django.urls import path, include
from rest_framework.routers import DefaultRouter

from grades.views import GradeViewSet

router = DefaultRouter()
router.register(r'grades', GradeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
