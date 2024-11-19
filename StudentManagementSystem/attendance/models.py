from django.db import models

from courses.models import Course
from students.models import Student


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10)  # For example: 'Present', 'Absent'

    class Meta:
        unique_together = ('student', 'course', 'date')  # A student can only have one attendance record per course per day

    def __str__(self):
        return f"{self.student.name} - {self.course.name} - {self.date} - {self.status}"
