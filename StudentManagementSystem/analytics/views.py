# analytics/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from analytics.models import APIRequestLog, CoursePopularity
from django.db.models import Count

class APIUsageReport(APIView):
    def get(self, request):
        most_active_users = (
            APIRequestLog.objects.values('user__username')
            .annotate(request_count=Count('id'))
            .order_by('-request_count')[:5]
        )
        most_popular_courses = (
            CoursePopularity.objects.order_by('-views')[:5]
        )
        data = {
            "most_active_users": list(most_active_users),
            "most_popular_courses": [
                {"course": course.course.name, "views": course.views}
                for course in most_popular_courses
            ],
        }
        return Response(data)
