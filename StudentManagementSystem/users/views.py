import logging
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from students.models import Student
from students.serializers import StudentSerializer
from .permissions import IsStudent, IsTeacher, IsAdmin
from users.serializers import CreateSerializer

# Logging setup
logger = logging.getLogger('django')


class StudentViewSet(viewsets.ModelViewSet):
    """
    API Viewset for managing student records.
    Accessible by students (for their own records) and teachers/admins.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        """
        Assign permissions dynamically based on user role.
        """
        permission_map = {
            'retrieve': [IsStudent()],
            'update': [IsStudent()],
            'partial_update': [IsStudent()],
            'destroy': [IsStudent()],
            'list': [IsTeacher() | IsAdmin()],
            'create': [IsTeacher() | IsAdmin()],
        }
        return permission_map.get(self.action, [IsAuthenticated()])

class RegistrationView(generics.CreateAPIView):
    """
    API View for user registration.
    """
    serializer_class = CreateSerializer
    permission_classes = [AllowAny]  # Anyone can register

    @swagger_auto_schema(
        operation_description="Register a new user with username, email, password, and role.",
        request_body=CreateSerializer,
        responses={
            201: "User  registered successfully.",
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
            logger.info(f"User  registered successfully: {user.username}, IP: {request.META.get('REMOTE_ADDR')}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f"Registration failed for {request.data.get('username')}: {serializer.errors}")
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)