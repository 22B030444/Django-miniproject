# grades/serializers.py

from rest_framework import serializers
from .models import Grade
from courses.models import Course
from students.models import Student


class GradeSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())


    grade_value = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    grade_letter = serializers.CharField(max_length=5, required=False, allow_blank=True)

    class Meta:
        model = Grade
        fields = ['id', 'student', 'course', 'grade_value', 'grade_letter', 'date', 'teacher']

    def validate(self, attrs):
        """
        Проверка, что хотя бы одно из полей grade_value или grade_letter заполнено.
        """
        if not attrs.get('grade_value') and not attrs.get('grade_letter'):
            raise serializers.ValidationError("At least one of 'grade_value' or 'grade_letter' must be provided.")
        return attrs

    def create(self, validated_data):
        """
        Создание новой оценки с учетом введенных данных.
        """
        return Grade.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Обновление существующей оценки.
        """
        instance.student = validated_data.get('student', instance.student)
        instance.course = validated_data.get('course', instance.course)
        instance.grade_value = validated_data.get('grade_value', instance.grade_value)
        instance.grade_letter = validated_data.get('grade_letter', instance.grade_letter)
        instance.date = validated_data.get('date', instance.date)
        instance.teacher = validated_data.get('teacher', instance.teacher)
        instance.save()
        return instance