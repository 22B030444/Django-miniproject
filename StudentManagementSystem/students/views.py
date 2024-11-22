from rest_framework.exceptions import PermissionDenied, NotFound
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from users.permissions import IsAdmin, IsStudent
import logging

logger = logging.getLogger('students')


class StudentViewSet(viewsets.ModelViewSet):
    """
    Viewset for students. Students can view and update only their own data.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        """
        Filter the queryset based on the user's role.
        """
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'STUDENT':
            logger.info(f"Student {user.username} accessing their own profile")
            return self.queryset.filter(user=user)
        logger.info(f"Unauthorized access attempt by user: {user.username}")
        raise PermissionDenied("You can only access your own data.")

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve student data with caching.
        """
        student_id = kwargs.get('pk')
        if not student_id:
            logger.warning('No student ID provided in retrieve request')
            return Response({"error": "Student ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f'student_profile_{student_id}'
        cached_student = cache.get(cache_key)

        if cached_student:
            logger.info(f'Cache hit for student ID: {student_id}')
            return Response(cached_student)

        try:
            student = self.get_object()
        except Student.DoesNotExist:
            logger.error(f'Student ID: {student_id} does not exist')
            raise NotFound("Student not found")

        serialized_student = self.get_serializer(student)
        cache.set(cache_key, serialized_student.data, timeout=300)
        logger.info(f'Student ID: {student_id} added to cache')

        return Response(serialized_student.data)

    def perform_update(self, serializer):
        """
        Update student data with permission checks and cache invalidation.
        """
        student = self.get_object()
        if student.user != self.request.user:
            logger.warning(f'Unauthorized update attempt by user: {self.request.user.username} on student ID: {student.id}')
            raise PermissionDenied("You can only edit your own data.")


        cache_key = f'student_profile_{student.id}'
        cache.delete(cache_key)
        logger.info(f'Cache cleared for student ID: {student.id}')
        serializer.save()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]  # Разрешить доступ аутентифицированным пользователям, включая администраторов
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsStudent()]
        return [IsAuthenticated()]