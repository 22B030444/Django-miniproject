from rest_framework import serializers
from courses.models import Course
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Student model.
    Allows for the representation and creation of student instances.
    """
    courses = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        many=True
    )
    dob = serializers.DateField(required=False, allow_null=True)  # Поле теперь не обязательно

    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'dob', 'registration_date', 'courses']

    def validate_email(self, value):
        """
        Validate that the email is unique and conforms to the expected format.
        """
        if Student.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        """
        Create a new Student instance with the validated data.
        """
        courses_data = validated_data.pop('courses', [])
        validated_data.setdefault('dob', "2000-01-01")  # Устанавливаем значение по умолчанию, если dob отсутствует
        student = Student.objects.create(**validated_data)
        student.courses.set(courses_data)  # Associate courses with the student
        return student
