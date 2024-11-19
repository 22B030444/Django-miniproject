from django.db import models
from StudentManagementSystem import settings
from courses.models import Enrollment
from users.models import CustomUser


class Student(models.Model):
    """
    Model representing a student in the Student Management System.
    """
    user = models.OneToOneField(CustomUser,
        on_delete=models.CASCADE,
        related_name="student_profile",
        null=True,
        blank=True
    )
    name = models.CharField(max_length=255, help_text="Full name of the student.")
    email = models.EmailField(unique=True, help_text="Unique email address of the student.")
    dob = models.DateField(help_text="Date of birth of the student.")
    registration_date = models.DateField(auto_now_add=True, help_text="Date when the student registered.")
    courses = models.ManyToManyField(
        'courses.Course',
        through='courses.Enrollment',
        help_text="Courses that the student is enrolled in."
    )

    def __str__(self):
        return self.name

    def clean(self):
        """
        Custom validation for the Student model.
        """
        super().clean()
        # Add any custom validation here if necessary

    def is_enrolled_in_course(self, course):
        return Enrollment.objects.filter(student=self, course=course).exists()