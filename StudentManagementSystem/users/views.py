# import logging
# from rest_framework import generics, status, viewsets
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from drf_yasg.utils import swagger_auto_schema
#
# from students.models import Student
# from students.serializers import StudentSerializer
# from .permissions import IsStudent, IsTeacher, IsAdmin
# from users.serializers import CreateSerializer
#
# # Logging setup
# logger = logging.getLogger('django')
#
#
# class StudentViewSet(viewsets.ModelViewSet):
#     """
#     API ViewSet for managing student records.
#     Accessible by students (for their own records) and teachers/admins.
#     """
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#
#     def get_queryset(self):
#         """
#         Return queryset based on user role:
#         - Students can only see their own records.
#         - Teachers and Admins can see all students.
#         """
#         user = self.request.user
#         if user.has_perm('students.view_all_students') or user.is_staff:
#             return Student.objects.all()
#         return Student.objects.filter(user=user)
#
#     def get_permissions(self):
#         """
#         Assign permissions dynamically based on user role.
#         """
#         if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
#             return [IsAuthenticated(), IsStudent()]
#         elif self.action in ['list', 'create']:
#             return [IsAuthenticated(), IsTeacher() | IsAdmin()]
#         return [IsAuthenticated()]
#
#     def perform_create(self, serializer):
#         """
#         Log the creation of a new student record.
#         """
#         student = serializer.save()
#         logger.info(f"Student created: {student.name}, by user: {self.request.user.username}")
#
#
# class RegistrationView(generics.CreateAPIView):
#     """
#     API View for user registration.
#     """
#     serializer_class = CreateSerializer
#     permission_classes = [AllowAny]  # Anyone can register
#
#     @swagger_auto_schema(
#         operation_description="Register a new user with username, email, password, and role.",
#         request_body=CreateSerializer,
#         responses={
#             201: "User registered successfully.",
#             400: "Validation error.",
#         }
#     )
#     def post(self, request, *args, **kwargs):
#         """
#         Override POST method to handle user registration.
#         """
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             logger.info(
#                 f"User registered successfully: {user.username}, Role: {user.role}, IP: {request.META.get('REMOTE_ADDR')}"
#             )
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         logger.warning(
#             f"Registration failed for {request.data.get('username', 'unknown user')}: {serializer.errors}"
#         )
#         return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
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
    API ViewSet for managing student records.
    Accessible by students (for their own records) and teachers/admins.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        """
        Return queryset based on user role.
        """
        user = self.request.user
        if hasattr(user, 'role') and user.role in ['Teacher', 'Admin']:
            return Student.objects.all()
        return Student.objects.filter(user=user)

    def get_permissions(self):
        """
        Assign permissions dynamically based on user role.
        """
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsStudent()]
        elif self.action in ['list', 'create']:
            return [IsAuthenticated(), IsTeacher() | IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Log the creation of a new student record.
        """
        student = serializer.save()
        logger.info(
            f"Student created: {student.name}, Email: {student.email}, "
            f"by user: {self.request.user.username}"
        )


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
            role = request.data.get('role')
            if not role:
                logger.warning("Role is required for registration.")
                return Response({'error': 'Role is required'}, status=status.HTTP_400_BAD_REQUEST)

            logger.info(
                f"User registered successfully: {user.username}, Role: {user.role}, "
                f"IP: {request.META.get('REMOTE_ADDR')}"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(
            f"Registration failed for {request.data.get('username', 'unknown user')}: {serializer.errors}"
        )
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
