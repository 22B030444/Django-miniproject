from rest_framework import serializers
from .models import Attendance
from courses.models import Course
from students.models import Student


class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'course', 'date', 'status']
