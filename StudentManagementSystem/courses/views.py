from rest_framework.decorators import action
from django.core.cache import cache
from rest_framework.generics import get_object_or_404

from students.models import Student
from users.permissions import IsStudent, IsAdmin
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
import logging
from rest_framework import viewsets
from rest_framework.response import Response

# Set up logger for courses app
logger = logging.getLogger('courses')

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Enrollment
from .serializers import EnrollmentSerializer

import logging

logger = logging.getLogger(__name__)

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [IsStudent()]
        elif self.action in ['update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        student = serializer.validated_data.get('student')
        course = serializer.validated_data.get('course')

        # Проверка существования объектов
        get_object_or_404(Student, pk=student.id)
        get_object_or_404(Course, pk=course.id)

        logger.info(f"Student {student.id} enrolled in course {course.id}")
        super().perform_create(serializer)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='by-instructor')
    def by_instructor(self, request):
        instructor_id = request.query_params.get('instructor_id')
        if instructor_id:
            courses = self.queryset.filter(instructor_id=instructor_id)
            serialized_courses = self.get_serializer(courses, many=True)
            return Response(serialized_courses.data)
        return Response({"error": "instructor_id parameter is required"}, status=400)

    def perform_create(self, serializer):
        # Логируем создание курса
        logger.info(f"Course {serializer.validated_data['name']} created.")
        super().perform_create(serializer)

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdmin()]  # Только администраторы могут добавлять, обновлять и удалять курсы
        return [IsAuthenticated()]  # Все аутентифицированные пользователи могут просматривать курсы

    def list(self, request, *args, **kwargs):
        instructor = request.query_params.get('instructor', None)
        student = request.query_params.get('student', None)

        # Construct cache key based on filters
        cache_key = f'course_list_instructor_{instructor}_student_{student}'

        # Check if cached data exists
        cached_courses = cache.get(cache_key)
        if cached_courses:
            return Response(cached_courses)

        # Filter courses by instructor or student (if parameters exist)
        if instructor:
            courses = self.queryset.filter(instructor=instructor)
        elif student:
            courses = self.queryset.filter(enrollments__student__id=student)  # Many-to-many relation
        else:
            courses = self.queryset.all()

        serialized_courses = self.get_serializer(courses, many=True)

        # Cache the courses for 10 minutes
        cache.set(cache_key, serialized_courses.data, timeout=600)

        return Response(serialized_courses.data)