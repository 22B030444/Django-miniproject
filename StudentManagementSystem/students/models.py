from django.db import models
from StudentManagementSystem import settings


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Refer to the custom user model
        on_delete=models.CASCADE,
        related_name="student_profile",
        null=True,
        blank=True
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    registration_date = models.DateField(auto_now_add=True)
    courses = models.ManyToManyField('courses.Course', through='courses.Enrollment')  # Link via Enrollment model

    def __str__(self):
        return self.name
