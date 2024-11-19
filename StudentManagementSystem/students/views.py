from rest_framework.exceptions import PermissionDenied
from django.core.cache import cache
from attendance.models import Attendance
from courses.models import Enrollment
from grades.models import Grade
from users.permissions import IsAdmin, IsStudent, IsTeacher
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
import logging

# Configure a logger for the students app
logger = logging.getLogger('students')


class AdminViewSet(viewsets.ModelViewSet):
    """
    Viewset for administrators. Allows full access to all student records.
    """
    permission_classes = [IsAuthenticated, IsAdmin, IsTeacher]  # Only admins can access
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_grades(self):
        """
        Get all grades. Can be extended for filtering by student or course.
        """
        return Grade.objects.all()

    def get_attendance(self):
        """
        Get all attendance records. Can be extended for filtering.
        """
        return Attendance.objects.all()

    def get_enrollments(self):
        """
        Get all enrollments. Useful for administrative tasks.
        """
        return Enrollment.objects.all()


class StudentViewSet(viewsets.ModelViewSet):
    """
    Viewset for students. Students can view and update only their own data.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsStudent]  # Only students

    def get_queryset(self):
        """
        Filter the queryset based on the user's role.
        """
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'STUDENT':
            return self.queryset.filter(user=user)
        return self.queryset  # Admins/teachers can see all students

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve student data. Implements caching for improved performance.
        """
        student_id = kwargs.get('pk')
        if not student_id:
            logger.warning('No student ID provided in retrieve request')
            return Response({"error": "Student ID is required"}, status=400)

        cache_key = f'student_profile_{student_id}'
        cached_student = cache.get(cache_key)

        if cached_student:
            logger.info(f'Cache hit for student ID: {student_id}')
            return Response(cached_student)

        try:
            student = self.get_object()
        except Student.DoesNotExist:
            logger.error(f'Student ID: {student_id} does not exist')
            return Response({"error": "Student not found"}, status=404)

        serialized_student = self.get_serializer(student)

        # Cache the student profile for 5 minutes
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

        # Invalidate the cache for the updated student
        cache_key = f'student_profile_{student.id}'
        cache.delete(cache_key)
        logger.info(f'Cache cleared for student ID: {student.id}')
        serializer.save()