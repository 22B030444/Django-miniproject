from django.db import models
from students.models import Student


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.CharField(max_length=255)  # You can use a foreign key if instructors are users

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # Ensure a student cannot enroll in the same course twice

    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.name}"
