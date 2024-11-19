# courses/serializers.py

from students.models import Student
from students.serializers import StudentSerializer
from .models import Course, Enrollment
from rest_framework import serializers

class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date']

    def validate(self, data):
        """
        Проверка на то, что студент не зачислен на этот курс.
        """
        student = data['student']
        course = data['course']
        if student.is_enrolled_in_course(course):  # Предполагается, что метод реализован в модели Student
            raise serializers.ValidationError("Student is already enrolled in this course.")
        return data

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