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
        dob = validated_data.get('dob', None)  # Убедитесь, что dob существует
        if dob is None:
            validated_data['dob'] = "2000-01-01"  # Установите значение по умолчанию
        student = Student.objects.create(**validated_data)
        student.courses.set(courses_data)  # Associate courses with the student
        return student
        student = Student.objects.create(**validated_data)
        student.courses.set(courses_data)  # Associate courses with the student
        return student