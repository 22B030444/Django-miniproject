# courses/serializers.py

from students.models import Student
from students.serializers import StudentSerializer
from .models import Course, Enrollment
from rest_framework import serializers

from rest_framework import serializers
from .models import Enrollment,Course

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date']

    def validate(self, attrs):
        student = attrs.get('student')
        course = attrs.get('course')

        # Дополнительная проверка
        if not Student.objects.filter(pk=student.id).exists():
            raise serializers.ValidationError({"student": "Student does not exist."})
        if not Course.objects.filter(pk=course.id).exists():
            raise serializers.ValidationError({"course": "Course does not exist."})

        return attrs

class CourseSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()  # Используем метод для получения студентов

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'instructor', 'students']

    def get_students(self, obj):
        """
        Получение списка студентов, зачисленных на курс.
        """
        students = obj.enrollments.values_list('student', flat=True)  # Получаем ID студентов
        return StudentSerializer(Student.objects.filter(id__in=students), many=True).data  # Сериализация студентов