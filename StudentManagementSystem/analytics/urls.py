# analytics/urls.py
from django.urls import path
from analytics.views import APIUsageReport

urlpatterns = [
    path('reports/', APIUsageReport.as_view(), name='api-usage-report'),
]
