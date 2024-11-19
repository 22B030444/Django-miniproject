import logging
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from students.models import Student
from students.serializers import StudentSerializer
from .serializers import RegistrationSerializer
from .permissions import IsStudent, IsTeacher, IsAdmin

# Logging setup
logger = logging.getLogger('django')


class StudentViewSet(viewsets.ModelViewSet):
    """
    API Viewset for managing student records.
    Accessible by students (for their own records) and teachers/admins.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]  # Permission classes will dynamically set below

    def get_permissions(self):
        """
        Assign permissions dynamically based on user role.
        """
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsStudent()]
        if self.action in ['list', 'create']:
            return [IsTeacher() or IsAdmin()]
        return super().get_permissions()


class RegistrationView(generics.CreateAPIView):
    """
    API View for user registration.
    """
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]  # Anyone can register

    @swagger_auto_schema(
        operation_description="Register a new user with username, email, password, and role.",
        request_body=RegistrationSerializer,
        responses={
            201: "User registered successfully.",
            400: "Validation error.",
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Override POST method to handle user registration.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User registered successfully: {user.username}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f"Registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
