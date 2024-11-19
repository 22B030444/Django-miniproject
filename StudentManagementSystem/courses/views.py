from requests import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.cache import cache
from .models import Course
from .serializers import CourseSerializer
import logging
from rest_framework.response import Response
# courses/views.py
from rest_framework import viewsets
from .models import Enrollment
from .serializers import EnrollmentSerializer


# Set up logger for courses app
logger = logging.getLogger('courses')


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def perform_create(self, serializer):
        # Log when a student is enrolled
        student = serializer.validated_data['student']
        course = serializer.validated_data['course']
        logger.info(f"Student {student.username} enrolled in course {course.name}")
        super().perform_create(serializer)


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def perform_create(self, serializer):
        # Log when a student is enrolled
        student = serializer.validated_data['student']
        course = serializer.validated_data['course']
        logger.info(f"Student {student.username} enrolled in course {course.name}")
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
        # Get the student and course from the validated data
        student = serializer.validated_data['student']
        course = serializer.validated_data['course']

        # Log the enrollment action
        logger.info(f"Student {student.username} enrolled in course {course.name}")

        # Perform the actual create action (save to the database)
        super().perform_create(serializer)
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]  # Only Admins can add/edit/delete courses
        return [IsAuthenticated()]  # Everyone can view courses

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
            courses = self.queryset.filter(students__id=student)  # Many-to-many relation
        else:
            courses = self.queryset.all()

        serialized_courses = self.get_serializer(courses, many=True)

        # Cache the courses for 10 minutes
        cache.set(cache_key, serialized_courses.data, timeout=600)

        return Response(serialized_courses.data)
