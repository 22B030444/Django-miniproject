from django.db import models

from courses.models import Course
from students.models import Student


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5)  # For example: 'A', 'B+', 'C', etc.
    date = models.DateField()
    teacher = models.CharField(max_length=255)

    class Meta:
        unique_together = ('student', 'course')  # A student can only have one grade per course

    def __str__(self):
        return f"{self.student.name} - {self.course.name} - {self.grade}"
