from django.contrib.auth import get_user_model
from rest_framework import serializers

from students.models import Student
from users.models import CustomUser

class CreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating users with an additional 'role' field.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},  # For security, password should not be readable
        }

    def validate_role(self, value):
        """
        Validate that the role is one of the defined choices.
        """
        if value not in dict(CustomUser .ROLE_CHOICES):
            raise serializers.ValidationError("Invalid role selected.")
        return value

    def create(self, validated_data):
        """
        Override the create method to handle user creation with a custom 'role' field.
        """
        # Удаляем роль из validated_data, чтобы не передавать её в create
        role = validated_data.pop('role')
        user = CustomUser (**validated_data)  # Создаем пользователя
        user.set_password(validated_data['password'])  # Устанавливаем зашифрованный пароль
        user.role = role  # Устанавливаем роль
        user.save()
        if role == 'STUDENT':
            Student.objects.create(user=user, name=user.username, email=user.email)
        return user


class DetailSerializer(serializers.ModelSerializer):
    """
    Serializer to display user details, e.g., for profile views.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']