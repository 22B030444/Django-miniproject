from rest_framework import serializers

from courses.serializers import CourseSerializer
from students.serializers import StudentSerializer
from .models import Attendance
from courses.models import Course
from students.models import Student


class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()  # Используем вложенный сериализатор
    course = CourseSerializer()  # Используем вложенный сериализатор

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'course', 'date', 'status']

    def validate_date(self, value):
        """
        Проверяет, что дата посещаемости не является будущей.
        """
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("Дата не может быть в будущем.")
        return value

    def create(self, validated_data):
        """
        Переопределяем метод создания, чтобы извлечь связанные объекты.
        """
        student_data = validated_data.pop('student')
        course_data = validated_data.pop('course')

        student = Student.objects.get(id=student_data['id'])
        course = Course.objects.get(id=course_data['id'])

        attendance = Attendance.objects.create(student=student, course=course, **validated_data)
        return attendance

    def update(self, instance, validated_data):
        """
        Переопределяем метод обновления, чтобы извлечь связанные объекты.
        """
        student_data = validated_data.pop('student', None)
        course_data = validated_data.pop('course', None)

        if student_data:
            instance.student = Student.objects.get(id=student_data['id'])
        if course_data:
            instance.course = Course.objects.get(id=course_data['id'])

        instance.date = validated_data.get('date', instance.date)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance