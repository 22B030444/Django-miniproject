# attendance/models.py

from django.db import models
from courses.models import Course
from students.models import Student

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'course', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.course.name} - {self.date} - {self.status}"

    def is_present(self):
        """Проверяет, присутствует ли студент."""
        return self.status == 'Present'

    def is_absent(self):
        """Проверяет, отсутствует ли студент."""
        return self.status == 'Absent'