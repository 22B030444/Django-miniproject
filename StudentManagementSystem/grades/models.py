# grades/models.py

from django.db import models
from courses.models import Course
from students.models import Student


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade_value = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Для числовых оценок
    grade_letter = models.CharField(max_length=5, null=True, blank=True)  # Для буквенных оценок
    date = models.DateField()
    teacher = models.CharField(max_length=255)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.name} - {self.course.name} - {self.grade_letter or self.grade_value} - {self.date}"

    def get_grade(self):
        """Returns the grade in a preferred format, e.g., letter or numerical."""
        return self.grade_letter if self.grade_letter else str(self.grade_value)