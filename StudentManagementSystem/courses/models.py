# courses/models.py

from django.db import models
from users.models import CustomUser


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)  # Связь с моделью User
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    credits = models.PositiveIntegerField(default=3)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Enrollment(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['enrollment_date']
    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.name} on {self.enrollment_date}"