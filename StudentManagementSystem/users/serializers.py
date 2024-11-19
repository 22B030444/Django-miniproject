from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from users.models import CustomUser


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Serializer for creating users with an additional 'role' field.
    """
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'role']
        extra_kwargs = {
            'password': {'write_only': True},  # For security, password should not be readable
        }

    def create(self, validated_data):
        """
        Override the create method to handle user creation with a custom 'role' field.
        """
        return CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
        )


class RegistrationSerializer(UserCreateSerializer):
    """
    Serializer for user registration with role support.
    """
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create method to handle user registration.
        """
        return get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
        )


class CustomUserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer to display user details, e.g., for profile views.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']
