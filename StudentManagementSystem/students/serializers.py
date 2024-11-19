from rest_framework import serializers
from courses.models import Course
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    # Use nested CourseSerializer if needed
    # from courses.serializers import CourseSerializer
    # courses = CourseSerializer(many=True)  # Uncomment if nested

    courses = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        many=True
    )

    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'dob', 'registration_date', 'courses']
