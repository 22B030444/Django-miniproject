# attendance/serializers.py

from rest_framework import serializers
from .models import Attendance
from courses.models import Course
from students.models import Student

class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())  # Ожидает только ID студента
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())  # Ожидает только ID курса

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'course', 'date', 'status']

    def validate_date(self, value):
        """
        Проверка, что дата посещаемости не является будущей.
        """
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("Дата не может быть в будущем.")
        return value

    def create(self, validated_data):
        """
        Переопределяем метод создания, чтобы извлечь связанные объекты.
        """
        student = validated_data.pop('student')  # Извлекаем student из validated_data
        course = validated_data.pop('course')  # Извлекаем course из validated_data

        # Создаем объект Attendance, передав правильные данные
        attendance = Attendance.objects.create(student=student, course=course, **validated_data)
        return attendance

    def update(self, instance, validated_data):
        """
        Переопределяем метод обновления, чтобы извлечь связанные объекты.
        """
        instance.student = validated_data.get('student', instance.student)
        instance.course = validated_data.get('course', instance.course)
        instance.date = validated_data.get('date', instance.date)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
