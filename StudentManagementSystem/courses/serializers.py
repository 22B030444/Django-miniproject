from students.models import Student
from students.serializers import StudentSerializer

from .models import Course

from rest_framework import serializers
from .models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    # You can customize the fields as needed
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date']  # Adjust fields as per your model

    def validate(self, data):
        # Optional: Add custom validation if needed
        if data['student'].is_enrolled_in_course(data['course']):  # Assuming you have a method to check this
            raise serializers.ValidationError("Student is already enrolled in this course.")
        return data


class CourseSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)  # Nested relationship

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'instructor', 'students']

    def get_students(self):
        from students.serializers import StudentSerializer

