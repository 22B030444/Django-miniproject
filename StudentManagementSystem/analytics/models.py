# analytics/models.py
from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()

class APIRequestLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.endpoint} ({self.method})"

class CoursePopularity(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    enrollments = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.course.name} - Views: {self.views}, Enrollments: {self.enrollments}"
